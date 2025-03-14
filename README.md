# 🌙 Bedtime Stories AI

An enchanting AI-powered bedtime story generator that creates warm, engaging stories with meaningful morals for children. This project aims to make bedtime storytelling a magical and educational experience, helping parents and caregivers share valuable life lessons through personalized stories.

## ✨ Features

- 🤖 AI-powered story generation
- 📚 Age-appropriate content
- 🎯 Customizable moral lessons
- 💫 Engaging and imaginative narratives
- 👶 Child-friendly themes

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- OpenAI API key
- Required Python packages:
  - openai==1.66.3
  - streamlit==1.43.2

To install the required packages, run:
```bash
pip install -r requirements.txt
```

## 📖 Usage

1. Set up your OpenAI API key in your Streamlit secrets:
   - Create a `.streamlit/secrets.toml` file
   - Add your API key: `OPENAI_API_KEY = "your-api-key-here"`

2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

3. Customize Your Story:
   - **Language Options** 🗣️
     - English: Traditional English storytelling
     - Hindi: Stories in Hindi
     - Hinglish: Natural mix of Hindi-English, written in Roman script
   
   - **Character Types** 🎭
     - People: Stories featuring human characters
     - Animals: Tales with animal characters (with realistic animal behaviors)
     - Both People & Animals: Interactive stories between humans and animals
   
   - **Moral Lessons** 🌟
     - Choose from: Kindness, Honesty, Sharing, Patience, Courage, 
       Friendship, Love, Respect, Responsibility, Gratitude, 
       Empathy, Hard Work, Consistency
   
   - **Cultural Contexts** 🌍
     - Available cultures: American, British, Indian, French, Spanish
     - Each story incorporates authentic cultural elements and traditions

4. Generate and Save:
   - Click "✨ Create Magical Story ✨" to generate your story
   - Use "🔄 Generate New Story" to create different versions
   - Download your favorite stories using "📥 Save Story"

💡 **Story Features:**
- Age-appropriate for children 2-5 years old
- 250-350 words in length (5-7 minutes reading time)
- Simple vocabulary and sentence structure
- Clear beginning, middle, and end
- 2-3 characters maximum
- Gentle, soothing language perfect for bedtime
- Cultural authenticity in storytelling style

## 🎯 Project Goals

- Create engaging and memorable stories that captivate young minds
- Impart valuable life lessons through storytelling
- Provide a helpful tool for parents and caregivers
- Ensure age-appropriate content and language
- Foster imagination and creativity

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Submit bug reports
- Propose new features
- Send pull requests

## 🙏 Acknowledgments

- Thanks to all contributors and supporters
- Inspired by the timeless tradition of bedtime storytelling


## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Bedtime Stories AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Note:** While the software is open-source, users are responsible for ensuring compliance with OpenAI's terms of service and proper handling of API keys.
