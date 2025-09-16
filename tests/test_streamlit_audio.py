"""
Test Streamlit audio components
Run with: streamlit run test_streamlit_audio.py
"""

import streamlit as st
import tempfile
import os
import librosa
import soundfile as sf
import numpy as np
import io

def test_audio_recording():
    """Test Streamlit's built-in audio recording widget"""
    
    st.header("🎤 Audio Recording Test")
    
    # Audio input widget (records audio)
    audio_file = st.audio_input("Record a short test message (5-10 seconds)")
    
    if audio_file is not None:
        st.success("✅ Audio recorded successfully!")
        
        # Get the raw bytes from the UploadedFile object
        audio_bytes = audio_file.getvalue()
        
        # Display audio info
        st.write(f"**Audio size:** {len(audio_bytes)} bytes")
        st.write(f"**File name:** {audio_file.name}")
        st.write(f"**File type:** {audio_file.type}")
        
        # Play back the recorded audio
        st.audio(audio_bytes, format="audio/wav")
        
        # Test audio processing
        try:
            # Save to temporary file for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_file_path = tmp_file.name
            
            # Process with librosa
            audio_data, sample_rate = librosa.load(tmp_file_path, sr=None)
            duration = len(audio_data) / sample_rate
            st.write(f"**Duration:** {duration:.2f} seconds")
            st.write(f"**Sample Rate:** {sample_rate} Hz")
            st.write(f"**Samples:** {len(audio_data)}")
            
            # Clean up
            os.unlink(tmp_file_path)
            
            st.success("✅ Audio processing successful!")
            
        except Exception as e:
            st.error(f"❌ Audio processing failed: {str(e)}")
    
    else:
        st.info("👆 Click the record button above to test audio recording")

def test_audio_upload():
    """Test audio file upload functionality"""
    
    st.header("📁 Audio File Upload Test")
    
    # File uploader widget
    uploaded_file = st.file_uploader(
        "Upload an audio file",
        type=["wav", "mp3", "m4a", "mp4", "webm", "ogg"]
    )
    
    if uploaded_file is not None:
        st.success("✅ File uploaded successfully!")
        
        # Display file info
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**File size:** {uploaded_file.size} bytes")
        st.write(f"**File type:** {uploaded_file.type}")
        
        # Play the uploaded audio
        st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
        
        # Test processing
        try:
            # Read file bytes
            file_bytes = uploaded_file.getvalue()
            
            # Save to temporary file for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(file_bytes)
                tmp_file_path = tmp_file.name
            
            # Process with librosa
            audio_data, sample_rate = librosa.load(tmp_file_path, sr=None)
            duration = len(audio_data) / sample_rate
            st.write(f"**Duration:** {duration:.2f} seconds")
            st.write(f"**Sample Rate:** {sample_rate} Hz")
            st.write(f"**Samples:** {len(audio_data)}")
            
            # Test resampling
            if sample_rate != 16000:
                st.info("Testing resampling for API compatibility...")
                audio_16k = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
                st.write(f"**Resampled:** 16kHz ({len(audio_16k)} samples)")
                st.success("✅ Resampling successful!")
            else:
                st.success("✅ Audio already at optimal sample rate!")
            
            # Clean up
            os.unlink(tmp_file_path)
            
        except Exception as e:
            st.error(f"❌ Audio processing failed: {str(e)}")
    
    else:
        st.info("👆 Upload an audio file to test processing")

def test_audio_playback():
    """Test audio playback controls"""
    
    st.header("▶️ Audio Playback Test")
    
    # Create sample audio data for testing
    if st.button("Generate Test Tone"):
        try:
            # Generate a simple test tone using numpy
            duration = 2.0  # seconds
            sample_rate = 22050
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            tone = 0.3 * np.sin(440 * 2 * np.pi * t)  # 440Hz sine wave
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                sf.write(tmp_file.name, tone, sample_rate)
                tmp_file_path = tmp_file.name
            
            # Read back as bytes for streamlit
            with open(tmp_file_path, 'rb') as f:
                audio_bytes = f.read()
            
            os.unlink(tmp_file_path)
            
            st.success("✅ Test tone generated!")
            st.audio(audio_bytes, format="audio/wav")
            
        except Exception as e:
            st.error(f"❌ Test tone generation failed: {str(e)}")

def main():
    st.title("🎵 Streamlit Audio Components Test")
    st.write("This test validates audio recording, upload, and playback functionality")
    
    # Test sections
    test_audio_recording()
    st.divider()
    
    test_audio_upload()
    st.divider()
    
    test_audio_playback()
    
    # Summary
    st.header("✅ Test Summary")
    st.write("""
    **What this test validates:**
    - ✅ Audio recording via microphone
    - ✅ Audio file upload (multiple formats)
    - ✅ Audio playback in browser
    - ✅ Audio processing with librosa
    - ✅ Resampling for API compatibility
    
    **If all tests pass, you're ready for audio development!**
    """)
    
    # Instructions for developers
    with st.expander("🛠️ Developer Notes"):
        st.code("""
        # To run this test:
        streamlit run test_streamlit_audio.py
        
        # Common issues:
        1. Microphone permissions - browser may ask for access
        2. Audio format compatibility - librosa handles most formats
        3. File size limits - Whisper API has 25MB limit
        4. Sample rate - API prefers 16kHz mono
        """)

if __name__ == "__main__":
    main()