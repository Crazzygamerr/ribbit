
Initial problem: 
 - Context size too big to parse the entire API response
 - API Documentation too large

Possible Solutions:
 - Truncate, Iterate or Summarize the repsponse
  	- The APIChain isn't capable of doing that, or modifying intermediate outputs
 - Split the task into generating the api url and parsing the response

Current Approach: 
 - Get the API url from parsing documents, possibly using Map Re-rank
   - https://github.com/sophiamyang/tutorials-LangChain/blob/main/LangChain_QA.ipynb
 - Fetch the url response and save the json as a file
   - Use the requests wrapper, see how it's implemented in api/base.py
 - Query the file using a JSON agent
   - https://python.langchain.com/docs/integrations/toolkits/json
 - I'm guessing that the current implementation in APIChain._call can be reused, it only has to be modified using this approach, instead of feeding the raw data
   - https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/chains/api/base.py#L125

Site to get docs: https://www.postman.com/miguelolave/workspace/nasa-open-apis/overview

- Code:
	- ~~Finalize format~~
  - ~~Fetch repo~~
- Data:
  - Gather docs
  - ~~Create Github Repo~~
- Submission:
  - READMEs for repo
  - Presentation

 Our challenge was to design a platform to explore open data that is available from NASA and other federal data repositories. We have developed Ribbit, an AI tool that enables users to chat with API documentation in a conversational format. It leverages our community-maintained API documentation repository, Tadpole-Docs, ensuring up-to-date information on NASA and other federal data repositories' API. The key features of our project are: 
 1) Generative AI capabilities
 2) Crowdsourced API Documentation 
 3) Question Answering on API Documentation
 4) Intuitive User Interface 
Our project enhances societal engagement, education, facilitates cross disciplinary research by enabling people to gain interdisciplinary insights and explore connections and patterns across diverse datasets that might be difficult to achieve manually.

Our project, Ribbit user-friendly platform for exploring open data from NASA and federal repositories. It simplifies data exploration through conversational AI, powered by a Language Learning Model. Ribbit offers real-time access to dataset from  multiple sources, and its crowdsourced documentation keeps the language model updated. With generative AI capabilities, it enhances societal engagement and cross-disciplinary research while providing a human-like interaction experience. In the future, Ribbit aims to scale up and facilitate rapid cross-disciplinary data exploration on a larger scale.

Our project, Ribbit, is an user -friendly platform which uses Tadpole-Docs. Tadpole-Docs enables the community to update the API documentation from the federal data repositories and Ribbit uses this updated API Documentation. The platform is powered by a Language Learning Model enabling it to have generative AI capabilities.  It enhances societal engagement and cross-disciplinary research while providing a human-like interaction.