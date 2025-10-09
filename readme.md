# ClarityNet - Explainable AI with Complete Transparency

ClarityNet is an intelligent AI assistant built with Streamlit that provides complete transparency in its decision-making process. It offers multimodal support for text, images, video, and audio inputs while explaining every reasoning step.

## ✨ Features

- **Multimodal Input Support**: Process text queries along with images, videos, and audio files
- **Intelligent Model Selection**: Automatically chooses between rapid and advanced AI models based on query complexity
- **Transparent Reasoning**: Provides detailed explanations of:
  - Input processing strategies
  - Model selection decisions
  - Answer construction logic
- **Smart Analysis**: Evaluates query complexity, technical depth, and media requirements
- **Rate Limiting**: Built-in API call management to prevent quota exhaustion
- **Response Caching**: Improves performance for repeated queries
- **Custom UI**: Beautiful space-themed interface with real-time processing indicators


## 🎯 Usage

1. **Ask Questions**: Type your query in the text area
2. **Upload Media** (optional):
   - Images (PNG, JPG, JPEG)
   - Videos (MP4, MOV, AVI)
   - Audio (MP3, WAV, OGG)
3. **Get Answers**: Receive AI-generated responses with complete transparency
4. **Understand the Process**: View detailed explanations of:
   - Why a specific model was chosen
   - How the input was processed
   - What factors influenced the answer

## ⚙️ Configuration

Edit `config.py` to customize:
- Model selection thresholds
- Technical keywords for complexity detection
- Generation parameters (temperature, tokens, etc.)
- File upload limits
- UI branding elements

## 🔧 Technical Details

### AI Models
- **Rapid Response Engine** (`gemini-2.0-flash`): Fast responses for straightforward queries
- **Advanced Reasoning Engine** (`gemini-2.5-pro`): Deep analysis for complex, technical, or multimodal queries

### Key Components

**ClarityNetEngine** (`backend.py`):
- Query analysis and complexity scoring
- Intelligent model selection
- Multimodal content processing
- Response generation with explanations
- Rate limiting and caching

**Streamlit Interface** (`app.py`):
- User input handling
- Media file uploads
- Real-time response display
- Explanation visualization
- Interactive UI components

## 🛡️ Rate Limiting

ClarityNet includes built-in rate limiting:
- **Rapid Model**: 15 calls per minute
- **Advanced Model**: 2 calls per minute

This prevents API quota exhaustion and provides user-friendly wait time messages.

## 📊 Explainability Features

ClarityNet provides transparency through:
- **Input Processing Strategy**: How your query and media are analyzed
- **Reasoning Architecture Selection**: Why a specific AI model was chosen
- **Answer Construction Decisions**: How the response was structured
- **Influencing Factors**: Key elements that shaped the output


## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/)
- Developed by Team XCEPTION'S

## 📧 Contact

For questions or feedback, reach out via [GitHub Issues](https://github.com/yourusername/claritynet/issues).
