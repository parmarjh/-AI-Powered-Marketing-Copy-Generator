import streamlit as st
import openai
import os
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
        import json
        result = json.loads(content)
        
        return result
    
    except Exception as e:
        return {
            "headline": f"Error generating content: {str(e)}",
            "description": "Please try again or check your API key.",
            "hashtags": [],
            "cta": ""
        }

def main():
    """
    Main function to run the Streamlit app
    """
    st.set_page_config(
        page_title="AI Marketing Copy Generator",
        page_icon="✨",
        layout="centered"
    )
    
    st.title("✨ AI Marketing Copy Generator")
    st.write("Generate engaging marketing copy tailored to your brand and audience")
    
    # Input form
    with st.form("input_form"):
        brand_name = st.text_input("Brand Name", placeholder="e.g., EcoGlow")
        
        product_description = st.text_area(
            "Product/Service Description",
            placeholder="e.g., Sustainable bamboo water bottles that keep drinks cold for 24 hours"
        )
        
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Eco-conscious young professionals who are active outdoors"
        )
        
        # Optional tone selection
        tone_options = ["Auto-detect", "Exciting", "Professional", "Casual"]
        selected_tone = st.selectbox("Tone of Voice", tone_options)
        
        submitted = st.form_submit_button("Generate Ad Copy")
    
    # Process submission
    if submitted:
        if not brand_name or not product_description or not target_audience:
            st.error("Please fill in all fields")
        else:
            with st.spinner("Generating your marketing copy..."):
                # Auto-detect tone if selected
                tone = None
                if selected_tone == "Auto-detect":
                    combined_text = f"{brand_name} {product_description} {target_audience}"
                    tone = analyze_sentiment(combined_text)
                    st.info(f"Detected tone: {tone}")
                elif selected_tone != "Auto-detect":
                    tone = selected_tone
                
                # Generate the ad copy
                result = generate_ad_copy(brand_name, product_description, target_audience, tone)
                
                # Display results in a nice format
                st.success("Your marketing copy is ready!")
                
                # Display headline
                st.subheader("Ad Headline:")
                st.markdown(f"### {result['headline']}")
                
                # Display description
                st.subheader("Marketing Description:")
                st.write(result['description'])
                
                # Display hashtags and CTA in columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Hashtags:")
                    for hashtag in result['hashtags']:
                        st.write(f"#{hashtag.replace('#', '').replace(' ', '')}")
                
                with col2:
                    st.subheader("Call to Action:")
                    st.write(result['cta'])
                
                # Add a download button for the copy
                copy_text = f"""
                # {result['headline']}
                
                {result['description']}
                
                Hashtags: {' '.join(['#' + h.replace('#', '').replace(' ', '') for h in result['hashtags']])}
                
                CTA: {result['cta']}
                """
                
                st.download_button(
                    label="Download Copy",
                    data=copy_text,
                    file_name=f"{brand_name}_marketing_copy.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
