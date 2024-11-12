import os
from dotenv import load_dotenv
from openai import OpenAI

class GrokMessageGenerator:
    def __init__(self):
        XAI_API_KEY = os.getenv("XAI_API_KEY")
        self.client = OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1",
        )
        self.SYSTEM_MESSAGE = "You are Grok, a helpful email content generator. You will follow the instructions given by the user exactly, without any deviation. Only generate the body of the email, do not add subject lines or sign off statements. Wrap the body in a <body> opening and closing tag. Do not add your own responses directed towards the user. Maintain a professional tone always. The general tone of the message can be cheerful, unless instructed otherwise. Do not generate content that can be considered offensive, inappropriate or phishing."

    def generate_message(self, user_message):

        user_msg_1 = "Generate an email selling my marketing services to this company: InnovaSoft located in India which sells these: software products. Emphasize my expertise marketing software products."
        assistant_message_1 = """'<body>\n'
 'Dear Team at InnovaSoft,\n'
 '\n'
 'I hope this email finds you well.\n'
 '\n'
 'I am writing to introduce you to the specialized marketing services I offer, '
 'which are tailored specifically for software product companies like yours. '
 'With over a decade of experience in the tech industry, I have successfully '
 'helped numerous software firms increase their visibility, drive sales, and '
 'establish a strong market presence.\n'
 '\n'
 '**Why Choose Me?**\n'
 '- **Industry Expertise:** My background in marketing software products gives '
 'me an in-depth understanding of the unique challenges and opportunities '
 'within this sector.\n'
 '- **Customized Strategies:** I develop bespoke marketing campaigns that '
 "align with your product's unique selling propositions, ensuring maximum "
 'impact.\n'
 '- **Proven Results:** My track record includes significant increases in lead '
 'generation, conversion rates, and customer retention for software '
 'companies.\n'
 '- **Holistic Approach:** From SEO and content marketing to social media '
 'strategies and PPC advertising, I cover all bases to ensure comprehensive '
 'market penetration.\n'
 '\n'
 '**What I Offer:**\n'
 '- **Market Analysis & Positioning:** Identifying your competitive edge and '
 'positioning your products effectively in the market.\n'
 '- **Branding & Messaging:** Crafting compelling narratives that resonate '
 'with your target audience.\n'
 '- **Lead Generation Campaigns:** Utilizing multi-channel approaches to '
 'attract and convert leads into customers.\n'
 '- **Performance Analysis:** Continuous monitoring and optimization of '
 'marketing efforts to ensure ROI.\n'
 '\n'
 'I am confident that with my expertise, InnovaSoft can achieve its growth '
 'objectives and stand out in the competitive Indian software market. I would '
 'love to discuss how my services can be tailored to meet your specific needs '
 'and goals.\n'
 '\n'
 'Please feel free to reach out to schedule a consultation at your earliest '
 'convenience. I am excited about the possibility of collaborating with '
 'InnovaSoft to drive your software products to new heights.\n </body>'"""
        completion = self.client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": self.SYSTEM_MESSAGE},
                {"role": "user", "content": user_msg_1},
                {"role": "assistant", "content": assistant_message_1},
                {"role": "user", "content": user_message},
            ],
        )

        return completion.choices[0].message

    def get_ai_message(self, user_message):
        ai_message = self.generate_message(user_message)
        body = ai_message.content
        #get text wrapped in <body> tag
        try:
            body = body[body.find("<body>")+6:body.find("</body>")]
        except:
            body = message.content
        
        return body 



if __name__=="__main__":
    gm = GrokMessageGenerator()
    user_message =  "Generate an email to this company: EcoGreen, informing them that their payment for their purchase of makeup products is pending since 1 month"
    message = gm.generate_message(user_message)
    
    
    # print(body)