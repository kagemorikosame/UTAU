import os
import json
from tkinter import Tk, Button, filedialog, messagebox
from pydub import AudioSegment  # インストール必須   $ pip install pydub


class UTAUTool:
    def __init__(self, root):
        self.root = root
        self.root.title("UTAU音源_結合・分割ソフト")
        self.create_widgets()

    def create_widgets(self):
        # 音源結合ボタン
        self.merge_button = Button(
            self.root, text="音源結合", command=self.merge_audio_files)
        self.merge_button.pack(pady=10)

        # 音源分割ボタン
        self.split_button = Button(
            self.root, text="音源分割", command=self.split_audio_files)
        self.split_button.pack(pady=10)

    def merge_audio_files(self):
        # フォルダ選択ダイアログを開く
        folder_path = filedialog.askdirectory(title="音源フォルダを選択")
        if not folder_path:
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
            # 復元情報を保存
            restore_data.append({
                "file_name": os.path.basename(audio_file),
                "duration": len(audio_segment)
            })

        # 結合した音源を保存
        output_path = filedialog.asksaveasfilename(
            defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if output_path:
            combined_audio.export(output_path, format="wav")
            # 復元情報を保存
            restore_file_path = output_path + ".json"
            with open(restore_file_path, 'w') as restore_file:
                json.dump(restore_data, restore_file)
            messagebox.showinfo("完了", "音源の結合と復元ファイルの保存が完了しました。")

    def split_audio_files(self):
        # 結合済みの音源ファイルを選択
        combined_audio_path = filedialog.askopenfilename(
            title="結合済み音源を選択", filetypes=[("WAV files", "*.wav")])
        if not combined_audio_path:
            return

        # 復元ファイルを選択
        restore_file_path = filedialog.askopenfilename(
            title="復元ファイルを選択", filetypes=[("JSON files", "*.json")])
        if not restore_file_path:
            return

        # 結合済みの音源をロード
        combined_audio = AudioSegment.from_file(combined_audio_path)

        # 復元ファイルを読み込む
        with open(restore_file_path, 'r') as restore_file:
            restore_data = json.load(restore_file)

        # 音源を分割して保存
        start = 0
        for data in restore_data:
            duration = data['duration']
            file_name = data['file_name']
            split_audio = combined_audio[start:start + duration]
            output_file_path = os.path.join(
                os.path.dirname(combined_audio_path), file_name)
            split_audio.export(output_file_path, format="wav")
            start += duration

        messagebox.showinfo("完了", "音源の分割が完了しました。")


if __name__ == "__main__":
    root = Tk()
    app = UTAUTool(root)
    root.mainloop()
