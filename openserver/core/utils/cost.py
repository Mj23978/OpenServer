
def completion_price_calculator(cost_prompt: float, cost_completion: float, prompt_token: int, completion_token: int):
    cost_inp = cost_prompt / 1000000 * prompt_token
    cost_out = cost_completion / 1000000 * completion_token
    return round(cost_inp + cost_out, 7)