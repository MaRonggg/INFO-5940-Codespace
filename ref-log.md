What did you learn from implementing a multi-agent workflow?
Technically, I learned how to implement multiple agents and connect them by using one agent’s response as the input for another. I also practiced adding tools to agents to enhance their functionalities. Moreover, I improved my ability to use Streamlit more professionally. Also, most importantly, I learned how to track which tools were being used by these agents so that I could ensure they were working in the way I designed. Meanwhile, it was impressive to see that we could connect different companies’ machine learning models using their API keys and various tools to work together toward the same goal. In addition, this workflow helped me realize that having multiple agents with different tools that can check each other’s results is beneficial. With more functionalities and additional layers of validation, the final output received by the user can be more reliable.

Challenges faced and how you addressed them.
One challenge I faced was ensuring that the reviewer agent used the internet search tool I designated, so I wrote a prompt to enforce it to use my tool instead of its own. The second challenge I faced was passing API keys to the agents. With inspiration from the TA, I directly placed my API key inside the .devcontainer/devcontainer.json file.


Any creative ideas, variations, or design choices (e.g., persona roles, prompt design).
For the planning agent, I first asked it to generate additional suggestions for situations where English-speaking users might face language barriers, since not every location’s official language is English. Next, I asked the agent to provide a list of regulations that users should pay attention to, as different locations, especially different countries, may have their own unique local regulations. Moreover, I also asked the agent to list the main local agencies that can help users exchange currency, since each location has its own currency and payment system.

GenAI assistance used and why.
I only used GenAI to help me correct grammar, since I’m not a native English speaker and can’t write perfectly in English.