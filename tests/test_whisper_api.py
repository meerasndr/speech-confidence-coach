"""
Test script for OpenAI Whisper API functionality
Run this to verify Whisper API access and audio processing capabilities
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import librosa
import soundfile as sf
import tempfile

def test_whisper_api():
    """Test OpenAI Whisper API transcription"""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print("🎤 Testing OpenAI Whisper API...")
    
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ ERROR: OPENAI_API_KEY not found in environment variables")
        print("Please set your API key in .env file")
        return False
    
    print("✅ API key found")
    
    # For this test, you'll need to provide a sample audio file
    # Create a simple test audio file or use an existing one
    test_audio_path = "data/sample_audio/test.wav"  # You'll need to create this
    
    if not os.path.exists(test_audio_path):
        print(f"⚠️  No test audio file found at {test_audio_path}")
        print("Please record a 5-10 second audio clip and save it as 'data/sample_audio/test.wav'")
        print("You can use any audio recording app or Audacity")
        return False
    
    try:
        # Test basic transcription
        with open(test_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        
        print("✅ Basic transcription successful:")
        print(f"   Transcript: '{transcript}'")
        
        # Test with timestamps
        with open(test_audio_path, "rb") as audio_file:
            transcript_with_timestamps = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        
        print("✅ Transcription with word timestamps successful:")
        print(f"   Duration: {transcript_with_timestamps.duration} seconds")
        print(f"   Word count: {len(transcript_with_timestamps.words) if transcript_with_timestamps.words else 0}")
        
        if transcript_with_timestamps.words:
            print("   Sample words with timestamps:")
            for word in transcript_with_timestamps.words[:3]:  # Show first 3 words
                print(f"     '{word.word}' at {word.start:.2f}s - {word.end:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_audio_processing():
    """Test audio file processing with librosa"""
    
    print("\n🔊 Testing audio processing...")
    
    test_audio_path = "data/sample_audio/test.wav"
    
    if not os.path.exists(test_audio_path):
        print("⚠️  Skipping audio processing test (no test file)")
        return True
    
    try:
        # Load audio file
        audio_data, sample_rate = librosa.load(test_audio_path, sr=None)
        
        print("✅ Audio file loaded successfully:")
        print(f"   Duration: {len(audio_data) / sample_rate:.2f} seconds")
        print(f"   Sample rate: {sample_rate} Hz")
        print(f"   Samples: {len(audio_data)}")
        
        # Test conversion to required format (if needed)
        # Whisper API prefers 16kHz mono
        if sample_rate != 16000:
            print("   Resampling to 16kHz...")
            audio_16k = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
            print("✅ Audio resampling successful")
            print(f"   New sample count: {len(audio_16k)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio processing error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== OpenAI Whisper API Test ===\n")
    
    whisper_success = test_whisper_api()
    audio_success = test_audio_processing()
    
    print(f"\n=== Test Results ===")
    print(f"Whisper API: {'✅ PASS' if whisper_success else '❌ FAIL'}")
    print(f"Audio Processing: {'✅ PASS' if audio_success else '❌ FAIL'}")
    
    if whisper_success and audio_success:
        print("\n🎉 All tests passed! Ready to proceed with development.")
    else:
        print("\n⚠️  Some tests failed. Please resolve issues before continuing.")