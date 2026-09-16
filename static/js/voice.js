/**
 * Multilingual Voice Recognition Module for Udhyami Yojna
 * Implements Web Speech API with feature detection, Indian locale support,
 * and graceful fallback when browser lacks native SpeechRecognition.
 */

export const INDIAN_LOCALES = [
  { code: 'hi-IN', label: 'हिन्दी (Hindi)' },
  { code: 'en-IN', label: 'English (India)' },
  { code: 'mr-IN', label: 'मराठी (Marathi)' },
  { code: 'ta-IN', label: 'தமிழ் (Tamil)' },
  { code: 'te-IN', label: 'తెలుగు (Telugu)' },
  { code: 'bn-IN', label: 'বাংলা (Bengali)' },
  { code: 'gu-IN', label: 'ગુજરાતી (Gujarati)' },
  { code: 'kn-IN', label: 'ಕನ್ನಡ (Kannada)' },
  { code: 'ml-IN', label: 'മലയാളം (Malayalam)' },
  { code: 'pa-IN', label: 'ਪੰਜਾਬੀ (Punjabi)' },
  { code: 'or-IN', label: 'ଓଡ଼ିଆ (Odia)' },
  { code: 'as-IN', label: 'অসমীয়া (Assamese)' }
];

export class VoiceManager {
  constructor(options = {}) {
    this.currentLocale = options.defaultLocale || 'hi-IN';
    this.onTranscriptUpdate = options.onTranscriptUpdate || (() => {});
    this.onStateChange = options.onStateChange || (() => {});
    this.onError = options.onError || (() => {});

    this.isRecording = false;
    this.recognition = null;
    this.finalTranscript = '';
    this.interimTranscript = '';

    // Feature Detection
    this.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || null;
    this.isSupported = Boolean(this.SpeechRecognition);
  }

  /**
   * Initializes the speech recognition engine if supported by browser.
   */
  init() {
    if (!this.isSupported) {
      console.warn('Web Speech API is not supported in this browser. Falling back to manual text input.');
      return false;
    }

    try {
      this.recognition = new this.SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = this.currentLocale;
      this.recognition.maxAlternatives = 1;

      this.recognition.onstart = () => {
        this.isRecording = true;
        this.onStateChange(true, 'Recording started. Speak into your microphone...');
      };

      this.recognition.onresult = (event) => {
        let interim = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          const transcriptChunk = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            this.finalTranscript += ' ' + transcriptChunk;
          } else {
            interim += transcriptChunk;
          }
        }
        this.interimTranscript = interim;
        const completeText = (this.finalTranscript + ' ' + this.interimTranscript).trim();
        this.onTranscriptUpdate(completeText, this.interimTranscript.length === 0);
      };

      this.recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        let errorMsg = 'Microphone or speech error encountered.';
        if (event.error === 'not-allowed') {
          errorMsg = 'Microphone access was denied. Please allow microphone permission in your browser address bar.';
        } else if (event.error === 'no-speech') {
          errorMsg = 'No speech detected. Please speak closer to your microphone.';
        } else if (event.error === 'network') {
          errorMsg = 'Speech network connectivity issue. Check your connection or type details manually.';
        }
        this.onError(errorMsg);
        this.stop();
      };

      this.recognition.onend = () => {
        if (this.isRecording) {
          // If still marked as recording, user didn't explicitly stop; restart if continuous desired
          try {
            this.recognition.start();
          } catch (e) {
            this.isRecording = false;
            this.onStateChange(false, 'Speech input paused.');
          }
        } else {
          this.onStateChange(false, 'Microphone idle.');
        }
      };

      return true;
    } catch (err) {
      console.error('Failed to configure SpeechRecognition:', err);
      this.isSupported = false;
      return false;
    }
  }

  setLocale(localeCode) {
    this.currentLocale = localeCode;
    if (this.recognition) {
      this.recognition.lang = localeCode;
    }
  }

  start() {
    if (!this.isSupported) {
      this.onError('Voice input is not supported in this browser. Please use the form or text box directly.');
      return false;
    }

    if (!this.recognition) {
      this.init();
    }

    try {
      this.isRecording = true;
      this.recognition.start();
      return true;
    } catch (e) {
      console.warn('SpeechRecognition start failed or already active:', e);
      return false;
    }
  }

  stop() {
    this.isRecording = false;
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {
        // Ignore stop error
      }
    }
    this.onStateChange(false, 'Microphone stopped.');
  }

  toggle() {
    if (this.isRecording) {
      this.stop();
      return false;
    } else {
      return this.start();
    }
  }

  clearTranscript() {
    this.finalTranscript = '';
    this.interimTranscript = '';
    this.onTranscriptUpdate('', true);
  }

  setTranscript(text) {
    this.finalTranscript = text;
    this.interimTranscript = '';
    this.onTranscriptUpdate(text, true);
  }
}
