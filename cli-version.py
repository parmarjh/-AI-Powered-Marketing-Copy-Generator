import argparse
import os
import json
import openai
from dotenv import load_dotenv
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Download NLTK resources for sentiment analysis
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_sentiment(text):
    """
    Analyze the sentiment of the provided text and return the dominant tone.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        str: Dominant tone (Exciting, Professional, or Casual)
    """
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    
    # Determine tone based on sentiment scores
    if sentiment_score['compound'] >= 0.5:
        return "Exciting"
    elif sentiment_score['pos'] > sentiment_score['neg'] and sentiment_score['neu'] > 0.6:
        return "Professional"
    else:
        return "Casual"

def generate_ad_copy(brand_name, product_description, target_audience, tone=None):
    """
    Generate marketing ad copy using OpenAI's GPT API.
    
    Args:
        brand_name (str): Name of the brand
        product_description (str): Description of the product/service
        target_audience (str): Target audience description
        tone (str, optional): Desired tone for the copy
        
    Returns:
        dict: Generated ad copy including headline, description, hashtags, and CTA
    """
    # Add tone instruction if provided
    tone_instruction = f" The tone should be {tone}." if tone else ""
    
    # Create prompt for OpenAI
    prompt = f"""
    Generate marketing content for the following:
    
    Brand Name: {brand_name}
    Product/Service Description: {product_description}
    Target Audience: {target_audience}{tone_instruction}
    
    Please provide:
    1. A short, catchy ad headline (maximum 10 words)
    2. A marketing description (2-3 sentences highlighting key benefits)
    3. Three relevant hashtags
    4. A compelling call-to-action phrase
    
    Format the response as JSON with keys: headline, description, hashtags, and cta.
    """
    
    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can use a different model if needed
            messages=[{"role": "system", "content": "You are a professional marketing copywriter who creates compelling, brand-appropriate ad copy."},
                     {"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # Extract the generated content
        content = response.choices[0].message.content
        
        # Parse JSON response
        result = json.loads(content)
        
        return result
    
    except Exception as e:
        return {
            "headline": f"Error generating content: {str(e)}",
            "description": "Please try again or check your API key.",
            "hashtags": [],
            "cta": ""
        }

def format_output(result):
    """Format the result dictionary for terminal display"""
    output = "\n" + "=" * 50 + "\n"
    output += f"📢 HEADLINE:\n{result['headline']}\n\n"
    output += f"📝 DESCRIPTION:\n{result['description']}\n\n"
    output += f"🏷️ HASHTAGS:\n" + " ".join([f"#{tag.replace('#', '').replace(' ', '')}" for tag in result['hashtags']]) + "\n\n"
    output += f"🔔 CALL TO ACTION:\n{result['cta']}\n"
    output += "=" * 50
    return output

def main():
    """Main function to run the CLI tool"""
    parser = argparse.ArgumentParser(description="AI Marketing Copy Generator")
    
    parser.add_argument('--brand', required=True, help="Brand name")
    parser.add_argument('--product', required=True, help="Product or service description")
    parser.add_argument('--audience', required=True, help="Target audience description")
    parser.add_argument('--tone', required=False, choices=["Exciting", "Professional", "Casual"], 
                       help="Tone of voice (optional)")
    
    args = parser.parse_args()
    
    print("\n🔍 Analyzing inputs...")
    
    # Auto-detect tone if not provided
    tone = args.tone
    if not tone:
        combined_text = f"{args.brand} {args.product} {args.audience}"
        tone = analyze_sentiment(combined_text)
        print(f"📊 Detected tone: {tone}")
    
    print("\n✨ Generating marketing copy...")
    result = generate_ad_copy(args.brand, args.product, args.audience, tone)
    
    print(format_output(result))
    
    # Ask if user wants to save to file
    save = input("\nSave this copy to a file? (y/n): ").lower()
    if save == 'y':
        filename = f"{args.brand.replace(' ', '_').lower()}_marketing_copy.txt"
        with open(filename, 'w') as f:
            f.write(f"HEADLINE: {result['headline']}\n\n")
            f.write(f"DESCRIPTION: {result['description']}\n\n")
            f.write(f"HASHTAGS: {' '.join(['#' + h.replace('#', '').replace(' ', '') for h in result['hashtags']])}\n\n")
            f.write(f"CALL TO ACTION: {result['cta']}")
        print(f"\n✅ Saved to {filename}")

if __name__ == "__main__":
    main()
