import os
import json
from tkinter import Tk, Button, filedialog, messagebox, Label, Toplevel, Text, Scrollbar, RIGHT, Y, END, Frame
from pydub import AudioSegment  # インストール必須   $ pip install pydub


class UTAUTool:
    def __init__(self, root):
        self.root = root
        self.root.title("UTAU音源_結合・分割ソフト")
        self.create_widgets()

    def create_widgets(self):
        # 音源結合ボタン
        self.merge_button = Button(
            self.root, text="音源結合", command=self.open_merge_window)
        self.merge_button.pack(pady=10)

        # 音源分割ボタン
        self.split_button = Button(
            self.root, text="音源分割", command=self.open_split_window)
        self.split_button.pack(pady=10)

    def open_merge_window(self):
        # 元のウィンドウを最小化
        self.root.withdraw()

        # 新しいウィンドウを作成
        merge_window = Toplevel(self.root)
        merge_window.title("音源結合 - ファイル選択")

        # ウィンドウが閉じられたときに元のウィンドウを表示する
        def on_close():
            self.root.deiconify()  # 元のウィンドウを表示
            merge_window.destroy()  # このウィンドウを閉じる

        merge_window.protocol("WM_DELETE_WINDOW", on_close)

        # 音源フォルダ選択ボタン
        folder_label = Label(merge_window, text="フォルダ未選択")
        folder_label.pack(pady=5)

        def select_folder():
            folder_path = filedialog.askdirectory(title="音源フォルダを選択")
            if folder_path:
                # ファイル名のみを表示
                folder_label.config(text=f"選択されたフォルダ: {
                                    os.path.basename(folder_path)}")
                merge_window.folder_path = folder_path

        select_folder_button = Button(
            merge_window, text="フォルダ選択", command=select_folder)
        select_folder_button.pack(pady=10)

        # 結合処理開始ボタン
        confirm_button = Button(merge_window, text="確認して結合",
                                command=lambda: self.confirm_merge(merge_window))
        confirm_button.pack(pady=10)

    def open_split_window(self):
        # 元のウィンドウを最小化
        self.root.withdraw()

        # 新しいウィンドウを作成
        split_window = Toplevel(self.root)
        split_window.title("音源分割 - ファイル選択")

        # ウィンドウが閉じられたときに元のウィンドウを表示する
        def on_close():
            self.root.deiconify()  # 元のウィンドウを表示
            split_window.destroy()  # このウィンドウを閉じる

        split_window.protocol("WM_DELETE_WINDOW", on_close)

        # 結合済み音源ファイル選択ボタン
        combined_audio_label = Label(split_window, text="音源ファイル未選択")
        combined_audio_label.pack(pady=5)

        def select_combined_audio():
            combined_audio_path = filedialog.askopenfilename(
                title="結合済み音源を選択", filetypes=[("WAV files", "*.wav")])
            if combined_audio_path:
                # ファイル名のみを表示
                combined_audio_label.config(
                    text=f"選択された音源: {os.path.basename(combined_audio_path)}")
                split_window.combined_audio_path = combined_audio_path

        combined_audio_button = Button(
            split_window, text="音源ファイル選択", command=select_combined_audio)
        combined_audio_button.pack(pady=5)

        # 復元ファイル選択ボタン
        restore_label = Label(split_window, text="復元ファイル未選択")
        restore_label.pack(pady=5)

        def select_restore_file():
            restore_file_path = filedialog.askopenfilename(
                title="復元ファイルを選択", filetypes=[("JSON files", "*.json")])
            if restore_file_path:
                # ファイル名のみを表示
                restore_label.config(text=f"選択された復元ファイル: {
                                     os.path.basename(restore_file_path)}")
                split_window.restore_file_path = restore_file_path

        restore_file_button = Button(
            split_window, text="復元ファイル選択", command=select_restore_file)
        restore_file_button.pack(pady=5)

        # 保存先フォルダ選択ボタン
        save_folder_label = Label(split_window, text="保存先フォルダ未選択")
        save_folder_label.pack(pady=5)

        def select_save_folder():
            save_folder_path = filedialog.askdirectory(title="保存先フォルダを選択")
            if save_folder_path:
                # フォルダ名のみを表示
                save_folder_label.config(
                    text=f"選択された保存先: {os.path.basename(save_folder_path)}")
                split_window.save_folder_path = save_folder_path

        save_folder_button = Button(
            split_window, text="保存先フォルダ選択", command=select_save_folder)
        save_folder_button.pack(pady=5)

        # 分割処理開始ボタン
        confirm_button = Button(split_window, text="確認して分割",
                                command=lambda: self.confirm_split(split_window))
        confirm_button.pack(pady=10)

    def confirm_merge(self, window):
        folder_path = getattr(window, 'folder_path', None)
        if not folder_path:
            messagebox.showerror("エラー", "フォルダが選択されていません。")
            return

        # 確認画面の表示
        audio_files = [f for f in os.listdir(
            folder_path) if f.endswith(('.wav', '.mp3'))]
        if not audio_files:
            messagebox.showerror("エラー", "選択したフォルダに音声ファイルが見つかりません。")
            return

        # 新しいウィンドウで確認メッセージを表示
        confirm_window = Toplevel(self.root)
        confirm_window.title("結合確認")
        confirm_window.geometry("300x300")  # ウィンドウサイズを固定

        # フレームを作成してスクロールバーとテキストウィジェットを配置
        frame = Frame(confirm_window)
        frame.pack(fill='both', expand=True)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        text_area = Text(frame, wrap='none',
                         yscrollcommand=scrollbar.set, width=40, height=15)
        text_area.pack(expand=True, fill='both')
        scrollbar.config(command=text_area.yview)

        # 確認メッセージを表示
        confirm_message = "次のファイルを結合します:\n" + "\n".join(audio_files)
        text_area.insert(END, confirm_message)
        text_area.config(state='disabled')  # テキストエリアを編集不可にする

        # 実行・キャンセルボタン
        confirm_button = Button(confirm_window, text="実行", command=lambda: [
                                self.merge_audio_files(window), confirm_window.destroy()])
        confirm_button.pack(pady=5)

        cancel_button = Button(confirm_window, text="キャンセル",
                               command=confirm_window.destroy)
        cancel_button.pack(pady=5)

    def confirm_split(self, window):
        combined_audio_path = getattr(window, 'combined_audio_path', None)
        restore_file_path = getattr(window, 'restore_file_path', None)
        save_folder_path = getattr(window, 'save_folder_path', None)

        if not combined_audio_path or not restore_file_path or not save_folder_path:
            messagebox.showerror("エラー", "すべてのファイルが選択されていません。")
            return

        # 新しいウィンドウで確認メッセージを表示
        confirm_window = Toplevel(self.root)
        confirm_window.title("分割確認")
        confirm_window.geometry("300x200")  # ウィンドウサイズを固定

        # フレームを作成してスクロールバーとテキストウィジェットを配置
        frame = Frame(confirm_window)
        frame.pack(fill='both', expand=True)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        text_area = Text(frame, wrap='none',
                         yscrollcommand=scrollbar.set, width=40, height=10)
        text_area.pack(expand=True, fill='both')
        scrollbar.config(command=text_area.yview)

        # 確認メッセージを表示
        confirm_message = f"音源ファイル: {os.path.basename(combined_audio_path)}\n復元ファイル: {os.path.basename(
            restore_file_path)}\n保存先: {os.path.basename(save_folder_path)}\nこれらのファイルで分割を行いますか？"
        text_area.insert(END, confirm_message)
        text_area.config(state='disabled')  # テキストエリアを編集不可にする

        # 実行・キャンセルボタン
        confirm_button = Button(confirm_window, text="実行", command=lambda: [
                                self.split_audio_files(window), confirm_window.destroy()])
        confirm_button.pack(pady=5)

        cancel_button = Button(confirm_window, text="キャンセル",
                               command=confirm_window.destroy)
        cancel_button.pack(pady=5)

    def merge_audio_files(self, window):
        folder_path = getattr(window, 'folder_path', None)
        if not folder_path:
            messagebox.showerror("エラー", "フォルダが選択されていません。")
            return

        # フォルダ内の音声ファイルを結合
        audio_files = [os.path.join(folder_path, f) for f in os.listdir(
            folder_path) if f.endswith(('.wav', '.mp3'))]
        if not audio_files:
            messagebox.showerror("エラー", "選択したフォルダに音声ファイルが見つかりません。")
            return

        combined_audio = AudioSegment.empty()
        restore_data = []

        for audio_file in audio_files:
            audio_segment = AudioSegment.from_file(audio_file)
            combined_audio += audio_segment
            restore_data.append({
                "file_name": os.path.basename(audio_file),
                "duration": len(audio_segment)
            })

        # 結合した音源を保存
        output_path = filedialog.asksaveasfilename(
            defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if output_path:
            combined_audio.export(output_path, format="wav")
            restore_file_path = output_path + ".json"
            with open(restore_file_path, 'w') as restore_file:
                json.dump(restore_data, restore_file)
            messagebox.showinfo("完了", "音源の結合と復元ファイルの保存が完了しました。")

    def split_audio_files(self, window):
        combined_audio_path = getattr(window, 'combined_audio_path', None)
        restore_file_path = getattr(window, 'restore_file_path', None)
        save_folder_path = getattr(window, 'save_folder_path', None)

        if not combined_audio_path or not restore_file_path or not save_folder_path:
            messagebox.showerror("エラー", "すべてのファイルが選択されていません。")
            return

        combined_audio = AudioSegment.from_file(combined_audio_path)

        with open(restore_file_path, 'r') as restore_file:
            restore_data = json.load(restore_file)

        start = 0
        for data in restore_data:
            duration = data['duration']
            file_name = data['file_name']
            split_audio = combined_audio[start:start + duration]
            output_file_path = os.path.join(save_folder_path, file_name)
            split_audio.export(output_file_path, format="wav")
            start += duration

        messagebox.showinfo("完了", "音源の分割が完了しました。")


if __name__ == "__main__":
    root = Tk()
    app = UTAUTool(root)
    root.mainloop()
