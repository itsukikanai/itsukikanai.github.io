import gradio as gr
import pandas as pd
import json
import os
from app.core import downloader, ai_analyzer, editor, database, utils, scanner

def create_ui():
    with gr.Blocks(title="AI Video Tool") as demo:
        gr.Markdown("# AI Video Tool")
        
        # Shared State
        current_video_id = gr.State(None)
        
        # --- Tab 1: Import ---
        with gr.Tab("インポート"):
            gr.Markdown("### URLから動画をダウンロード")
            with gr.Row():
                url_input = gr.Textbox(label="動画URL", placeholder="https://youtube.com/watch?v=...", scale=4)
                download_btn = gr.Button("ダウンロード", variant="primary", scale=1)
            
            with gr.Row():
                 format_radio = gr.Radio(["Video", "Audio"], label="フォーマット", value="Video")
                 res_dropdown = gr.Dropdown(["best", "1080p", "720p", "480p"], label="最大解像度", value="best")
                 auto_transcribe_chk = gr.Checkbox(label="字幕もダウンロード (yt-dlp)", value=True)

            dl_output = gr.Textbox(label="ログ", interactive=False)
            
            def handle_download(url, fmt, res, auto_transcribe, progress=gr.Progress()):
                try:
                    mode = 'audio' if fmt == 'Audio' else 'video'
                    msg, new_id = downloader.download_video(url, format_mode=mode, resolution=res, progress=progress)
                    
                    return msg
                except Exception as e:
                    return f"Error: {str(e)}"
            
            download_btn.click(handle_download, inputs=[url_input, format_radio, res_dropdown, auto_transcribe_chk], outputs=[dl_output])

        # --- Tab 2: Library (Gallery & Search) ---
        with gr.Tab("ライブラリ"):
            with gr.Row():
                search_bar = gr.Textbox(label="検索 (テキストまたはタイトル)", placeholder="キーワードを入力...", scale=4)
                search_btn = gr.Button("検索", scale=1)
                refresh_btn = gr.Button("ギャラリー更新", scale=1)
            
            # Mode Switch: Gallery vs Search Results
            with gr.Row():
                # Tag Filter
                tag_filter = gr.Dropdown(label="タグでフィルタ", choices=[], multiselect=True, interactive=True)
                
            with gr.Row():
                gallery_view = gr.Gallery(label="動画ライブラリ", columns=4, height="auto")
                # Search Results: Video Title, Start Time, Text, _VideoID, _StartSeconds, _EndSeconds
                search_results = gr.Dataframe(
                    headers=["動画", "時間", "テキスト", "db_id", "start_sec", "end_sec"],
                    datatype=["str", "str", "str", "number", "number", "number"],
                    visible=False,
                    interactive=False,
                    label="検索結果 (行を選択してモンタージュ作成)"
                )
            
            # Actions for Search Results
            with gr.Row(visible=False) as search_actions_row:
                play_clip_btn = gr.Button("選択したクリップを再生")
                create_montage_btn = gr.Button("検索結果からモンタージュを作成")
            
            # Player
            video_player = gr.Video(label="プレビュー")
            
            # Helper to load gallery
            def load_gallery(tags=None):
                if tags:
                    videos = database.get_videos_by_tags(tags)
                else:
                    videos = database.get_all_videos()
                
                # Gallery items
                items = []
                for v in videos:
                    # Check thumbnail
                    thumb = v.get('thumbnail_path')
                    if thumb and os.path.exists(thumb):
                        path = thumb
                    else:
                        # Use placeholder if video path is used it might crash Gradio Gallery or be slow
                        # path = v['file_path'] 
                        path = os.path.abspath("assets/placeholder.svg")
                        
                    label = v['title']
                    items.append((path, label))
                
                # Update choices
                all_tags = database.get_all_tags()
                
                return items, gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(choices=all_tags)

            refresh_btn.click(load_gallery, inputs=[tag_filter], outputs=[gallery_view, gallery_view, search_results, search_actions_row, tag_filter])
            tag_filter.change(load_gallery, inputs=[tag_filter], outputs=[gallery_view, gallery_view, search_results, search_actions_row, tag_filter])
            
            # Search Logic
            def handle_search(query):
                if not query:
                    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False) # Show Gallery
                
                results = database.search_subtitles(query)
                # Helper to format
                data = []
                for r in results:
                    data.append([
                        r['video_title'],
                        utils.format_timestamp(r['start_time']),
                        r['text'],
                        r['video_id'], # video_id (db id) needed or video_uid? video_id FK in subtitles is videos.id
                        r['start_time'],
                        r['end_time']
                    ])
                
                return gr.update(visible=False), gr.update(visible=True, value=data), gr.update(visible=True) # Hide Gallery, Show Search

            search_btn.click(handle_search, inputs=[search_bar], outputs=[gallery_view, search_results, search_actions_row])
            search_bar.submit(handle_search, inputs=[search_bar], outputs=[gallery_view, search_results, search_actions_row])

            # Play Clip
            def play_selected_clip(evt: gr.SelectData, df_data):
                # evt.index is [row, col]
                row_idx = evt.index[0]
                # Get data from dataframe
                # df_data is fully loaded? 
                # Gradio passes the whole dataframe value if inputs=[search_results]
                try:
                    row = df_data.iloc[row_idx]
                    vid_db_id = int(row[3])
                    start = float(row[4])
                    end = float(row[5])
                    
                    video = database.get_video_by_id(vid_db_id)
                    # Temp preview
                    clips = [{'video_path': video['file_path'], 'start': start, 'end': end}]
                    out = editor.create_montage(clips, output_filename=f"preview_search_{vid_db_id}_{row_idx}.mp4", fast_preview=True)
                    return out
                except Exception as e:
                    print(e)
                    return None

            # search_results.select(play_selected_clip, inputs=[search_results], outputs=[video_player]) 
            # Note: select triggers on cell click.
            # We need a button to "Play" maybe, or just click.
            # Let's use the button "Play Selected Clip" which reads selected rows? 
            # Gradio Dataframe doesn't output "selected rows" explicitly unless selectable=True and using state.
            # Actually, using `select` event is best for single click.
            search_results.select(play_selected_clip, inputs=[search_results], outputs=[video_player])

            # Montage
            def handle_montage(df_data):
                # How to get selected rows? 
                # If dataframe doesn't support multi-select easily in UI return, we assume ALL visible rows?
                # Or we prompt user to filter?
                # "Create Montage from Search Results" (All)
                # Let's just do all rows in current view for simplicity of MVP.
                clips = []
                for _, row in df_data.iterrows():
                    video_db_id = int(row[3])
                    video = database.get_video_by_id(video_db_id)
                    clips.append({
                        'video_path': video['file_path'],
                        'start': row[4],
                        'end': row[5]
                    })
                
                if not clips:
                    return None
                
                out_path = editor.create_montage(clips, output_filename="search_montage.mp4")
                return out_path

            create_montage_btn.click(handle_montage, inputs=[search_results], outputs=[video_player])

            # Gallery Select -> Actions
            # When clicking a gallery item, we want to maybe go to Editor tab? 
            # Or show actions?
            with gr.Row(visible=True) as gallery_actions:
                analyze_btn = gr.Button("AI分析・編集画面へ") 
                # Actions disabled since Whisper is removed
                transcribe_btn = gr.Button("文字起こし実行 (廃止)", interactive=False, visible=False)
                export_sub_btn = gr.Button("字幕エクスポート (廃止)", interactive=False, visible=False)
                delete_btn = gr.Button("動画削除", variant="stop")
            
            export_file = gr.File(label="字幕ダウンロード", visible=False, interactive=False)
            
            selected_video_idx = gr.State(None) # Index in db list
            
            def on_gallery_select(evt: gr.SelectData):
                # evt.index is the index of image
                # We need to map back to DB ID.
                # Simplest way: re-fetch videos list inside locally or store in state.
                videos = database.get_all_videos()
                if evt.index < len(videos):
                    vid = videos[evt.index]
                    return vid['id'], f"Selected: {vid['title']}"
                return None, "Error selection"

            gallery_status = gr.Textbox(label="ステータス", interactive=False)
            gallery_view.select(on_gallery_select, outputs=[current_video_id, gallery_status])
            
            # Delete Action
            def trigger_delete(vid_id):
                if not vid_id:
                     # gallery_view, gallery_view, search_results, search_actions_row, tag_filter, gallery_status
                    return gr.skip(), gr.skip(), gr.skip(), gr.skip(), gr.skip(), "No video selected."
                
                database.delete_video(vid_id)
                # Returns 5 items from load_gallery + 1 status message
                return load_gallery() + ("Deleted video.",)

            delete_btn.click(trigger_delete, inputs=[current_video_id], outputs=[gallery_view, gallery_view, search_results, search_actions_row, tag_filter, gallery_status])

        # --- Tab 3: Editor ---
        with gr.Tab("編集・分析"):
            gr.Markdown("### AI分析 & 編集")
            # Inputs: Select Video (or use globally selected)
            # But we might want a dropdown here too.
            video_dropdown = gr.Dropdown(label="動画を選択", choices=[], interactive=True)
            
            def update_dropdown():
                videos = database.get_all_videos()
                print(f"DEBUG: update_dropdown found {len(videos)} videos.")
                new_choices = [(f"{v['title']} (ID: {v['id']})", v['id']) for v in videos]
                return gr.Dropdown(choices=new_choices, interactive=True)

            refresh_editor_btn = gr.Button("リスト更新")
            refresh_editor_btn.click(update_dropdown, outputs=[video_dropdown])
            
            # Analysis
            analyze_action_btn = gr.Button("AI分析を実行")
            
            # Highlights Editor
            highlights_df = gr.Dataframe(
                headers=["start", "end", "score", "description"],
                datatype=["number", "number", "number", "str"],
                label="ハイライト (編集可)",
                interactive=True
            )
            
            # Preview Row
            preview_btn = gr.Button("ハイライトをプレビュー")
            editor_player = gr.Video(label="クリッププレビュー")
            
            # Montage/Export
            export_btn = gr.Button("ハイライトを動画として書き出し")
            export_output = gr.Video(label="書き出された動画")
            
            # Load Analysis
            def load_analysis(vid_id):
                if not vid_id: return None
                vid = database.get_video_by_id(vid_id)
                if vid and vid['analysis_result']:
                    try:
                        data = json.loads(vid['analysis_result'])
                        hl = data.get('highlights', [])
                        # Convert to List of lists, ensuring start < end
                        rows = []
                        for h in hl:
                            s = h.get('start_time', 0)
                            e = h.get('end_time', 0)
                            rows.append([min(s, e), max(s, e), h.get('score', 0), h.get('description', '')])
                        return rows
                    except:
                        pass
                return []

            video_dropdown.change(load_analysis, inputs=[video_dropdown], outputs=[highlights_df])
            
            def run_analysis(vid_id, progress=gr.Progress()):
                if not vid_id: return None
                res = ai_analyzer.analyze_video(vid_id, progress=progress)
                hl = res.get('highlights', [])
                rows = [[h['start_time'], h['end_time'], h['score'], h['description']] for h in hl]
                return rows
            
            analyze_action_btn.click(run_analysis, inputs=[video_dropdown], outputs=[highlights_df])
            
            def preview_highlight(evt: gr.SelectData, df_data, vid_id):
                # row index
                row_idx = evt.index[0]
                row = df_data.iloc[row_idx]
                start = float(row['start'])
                end = float(row['end'])
                vid = database.get_video_by_id(vid_id)
                
                # Temp preview
                clips = [{'video_path': vid['file_path'], 'start': start, 'end': end}]
                out = editor.create_montage(clips, output_filename=f"preview_{vid_id}_{row_idx}.mp4", fast_preview=True)
                return out

            highlights_df.select(preview_highlight, inputs=[highlights_df, video_dropdown], outputs=[editor_player])
            
            def export_highlights(df_data, vid_id, progress=gr.Progress()):
                if not vid_id: return None
                vid = database.get_video_by_id(vid_id)
                clips = []
                for _, row in df_data.iterrows():
                    clips.append({
                        'video_path': vid['file_path'],
                        'start': row['start'],
                        'end': row['end']
                    })
                return editor.create_montage(clips, output_filename=f"montage_{vid_id}.mp4", progress=progress)

            export_btn.click(export_highlights, inputs=[highlights_df, video_dropdown], outputs=[export_output])

        # --- Tab 4: Settings ---
        with gr.Tab("設定"):
            gr.Markdown("### 設定")
            with gr.Row():
                api_key_gemini = gr.Textbox(label="Gemini API Key", type="password")
                api_key_openai = gr.Textbox(label="OpenAI API Key", type="password")
            
            save_config_btn = gr.Button("設定を保存")
            config_status = gr.Textbox(label="ステータス", interactive=False)
            
            def load_current_config():
                # Load from .env or config
                # Actually .env is loaded by python-dotenv, but we might want to edit it?
                # Editing .env file directly for now.
                return "", "" # Security: maybe don't show existing keys?

            def save_keys(key_gemini, key_openai):
                # Write to .env
                # Simple append or replace
                content = f"API_KEY_GEMINI={key_gemini}\nAPI_KEY_OPENAI={key_openai}\n"
                with open(".env", "w") as f:
                    f.write(content)
                # Reload env?
                from dotenv import load_dotenv
                load_dotenv(override=True)
                return "設定を保存しました。"

            save_config_btn.click(save_keys, inputs=[api_key_gemini, api_key_openai], outputs=[config_status])
            
            gr.Markdown("### ストレージ管理")
            scan_btn = gr.Button("ストレージを再スキャンして動画をインポート")
            scan_status = gr.Textbox(label="スキャン結果", interactive=False)
            
            def handle_scan(progress=gr.Progress()):
                return scanner.scan_and_import_videos(progress=progress)
            
            scan_btn.click(handle_scan, outputs=[scan_status])
             
        # Initial Load
        demo.load(load_gallery, outputs=[gallery_view, gallery_view, search_results, search_actions_row, tag_filter])
        demo.load(update_dropdown, outputs=[video_dropdown])
             
    return demo
