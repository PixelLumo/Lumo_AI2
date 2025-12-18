# Piper TTS Setup Instructions

## Folder Structure Created
```
C:\Lumo_AI\audio\piper\
├── piper.exe
├── en_US-lessac-medium.onnx
└── en_US-lessac-medium.onnx.json
```

✅ **Folder created:** `audio/piper/`

## What You Need to Do Next

You need to download the Piper TTS executable and voice model files and place them in the `audio/piper/` directory.

### Download Links

**Option 1: Download Pre-Built Binary (Recommended)**

1. Go to: https://github.com/rhasspy/piper/releases
2. Download the latest Windows release (e.g., `piper-1.2.0-windows-x86_64.zip`)
3. Extract `piper.exe` to `C:\Lumo_AI\audio\piper\`

**Option 2: Install via Python**
```bash
pip install piper-tts
# Then copy the piper executable to audio/piper/
```

### Download Voice Model

1. Go to: https://huggingface.co/rhasspy/piper-voices/tree/main
2. Find `en_US-lessac-medium`
3. Download:
   - `en_US-lessac-medium.onnx` (269 MB)
   - `en_US-lessac-medium.onnx.json` (1.5 KB)
4. Place both files in `C:\Lumo_AI\audio\piper\`

### Expected Final Structure

```
C:\Lumo_AI\audio\piper\
├── piper.exe                        (executable)
├── en_US-lessac-medium.onnx         (269 MB)
└── en_US-lessac-medium.onnx.json    (config)
```

### Verify Installation

```powershell
cd C:\Lumo_AI
ls audio\piper\
```

Should show:
```
    Directory: C:\Lumo_AI\audio\piper

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----   [date]      [time]         [size] piper.exe
-a----   [date]      [time]     281268224 en_US-lessac-medium.onnx
-a----   [date]      [time]           1563 en_US-lessac-medium.onnx.json
```

### Test Piper

Once files are in place, test with:
```powershell
cd C:\Lumo_AI\audio\piper
.\piper.exe --help
```

---

**Status:** ✅ Folder structure ready, waiting for files

Once you place the files, LUMO's TTS (Text-to-Speech) will work locally! 🔊

