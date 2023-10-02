
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
 