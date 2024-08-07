QAPROMPT = """You are a expert scientist. Given the following unformatted text from an academic paper, please find the answer to a question.\n
    
    Question: {question}

    text: {chunks}

    If you find multiple answers, please provide the most relevant answer. \n
    Also provide the text which was used to generate the answer. \n
    Important: If you couldn't find an answer, reply with 'not found'

    You can also use previous questions and answers to help you generate the answer. \n
    Previous:
    {previous} \n

    answer: <provide answer here>
    literature evidence: <provide text here>
    
    Format instructions: \n{format_instructions}
        
    """
    