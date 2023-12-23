import requests

class Functions:

    @staticmethod
    def get_images_by_agent_id(agent_id):
        # Create a list of lists to store image path and base64 data
        image_list = []
        api_url = f"http://127.0.0.1:8000/imagesbyagentid/{agent_id}"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            json_data = response.json()

            for data in json_data:
                if 'base64_Image' in data and 'path' in data:
                    # Add a list with path and base64 image to the image_list
                    image_list.append([data['path'], data['base64_Image']])

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")

        return image_list
    
    @staticmethod
    def get_images_by_base_id(id):
        agent_id = ""
        api_url = f"http://127.0.0.1:8000/image/{id}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            json_data = response.json()

            if 'agent_id' in json_data:
                agent_id = json_data['agent_id']
                return Functions.get_images_by_agent_id(agent_id)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")

        return response
    

    @staticmethod
    def get_baseids():
        api_url = "http://127.0.0.1:8000/baseimages/"
        response = requests.get(api_url)
        Baseids = []

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()
            for data in json_data:
                # Check if the 'base64_Image' node exists in the JSON data
                if 'id' in data:
                    id = data['id']
                    Baseids.append(id)
        return Baseids
    
    @staticmethod
    def get_baseimage(id):
        api_url = "http://127.0.0.1:8000/baseimage/"+str(id)
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()
            # Check if the 'base64_Image' node exists in the JSON data
            print(json_data)
            if 'base64' in json_data:
                base64_Image = json_data['base64']
                print(base64_Image)
                return base64_Image
    

