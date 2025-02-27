# AI-Powered Marketing Copy Generator

This application generates personalized marketing copy for brands based on product descriptions and target audiences. It leverages OpenAI's GPT API to create engaging ad headlines, marketing descriptions, hashtags, and calls-to-action.

## Features

- **Personalized Ad Copy**: Generate tailored marketing content based on brand name, product/service description, and target audience
- **Tone Selection**: Choose from predefined tones (Exciting, Professional, Casual) or use auto-detection
- **Sentiment Analysis**: Automatically detect the appropriate tone from your inputs
- **Multi-output**: Generates ad headlines, descriptions, hashtags, and CTAs
- **User-friendly Interface**: Simple Streamlit web interface
- **Downloadable Results**: Save your generated copy as a text file

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/ai-marketing-copy-generator.git
cd ai-marketing-copy-generator
```

2. Create and activate a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Run the Streamlit application:
```
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Fill in the form with:
   - Brand Name
   - Product/Service Description
   - Target Audience
   - Desired Tone (or use auto-detect)

4. Click "Generate Ad Copy" to create your marketing content

5. View the generated content and download it if desired

## Command Line Interface (Alternative)

If you prefer using a command line interface, you can run:

```
python cli.py --brand "Brand Name" --product "Product Description" --audience "Target Audience" --tone "Exciting"
```

The `--tone` parameter is optional and will auto-detect if not provided.

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection (for API calls)
- Required Python packages (see requirements.txt)

## Customization

You can modify the code to:
- Use different OpenAI models
- Adjust temperature settings for creativity
- Add additional output types
- Customize the UI layout and styling

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- OpenAI for providing the GPT API
- Streamlit for the web application framework
- NLTK for sentiment analysis capabilities
