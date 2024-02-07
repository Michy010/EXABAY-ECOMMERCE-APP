# # integrations/utils.py
# from portalsdk import APIContext, APIMethodType, APIRequest

# def generate_session_key_tanzania():
#     api_context = APIContext()
#     api_context.api_key = 'your_api_key'  # Replace with your API key
#     api_context.public_key = 'your_public_key'  # Replace with your public key
#     api_context.ssl = True
#     api_context.method_type = APIMethodType.GET
#     api_context.address = 'openapi.m-pesa.com'
#     api_context.port = 443
#     api_context.path = '/sandbox/ipg/v2/vodacomTZN/getSession/'  # Updated path for Vodacom Tanzania

#     api_context.add_header('Origin', '*')

#     api_request = APIRequest(api_context)

#     result = None
#     try:
#         result = api_request.execute()
#     except Exception as e:
#         print('Call Failed: ' + str(e))

#     if result is None:
#         raise Exception('SessionKey call failed to get result. Please check.')

#     return result.body['output_SessionID']
