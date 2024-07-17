from PIL import Image
import requests
import os

api_key = 'YaU90zVmxTGuHsWNZWawWP5QTOpDYyWP'

# face matching
def faceMatching(img_selfie, pre_img_path):
    headers = {'api_key': api_key}
    files = [
        ('file[]', open(img_selfie, 'rb')),
        ('file[]', open(pre_img_path, 'rb'))
    ]
    response = requests.post('https://api.fpt.ai/dmp/checkface/v1', headers=headers, files=files)
    check = {
        'similarity':response.json()['data']['similarity'],
        'isMatch':response.json()['data']['isMatch']
    }
    return check

# extract information
def extractInfo(pre_img_path, behind_img_path):
    pre_img = {'image': open(pre_img_path, 'rb').read()}
    behind_img = {'image': open(behind_img_path, 'rb').read()}
    headers = {
        'api-key': api_key
    }

    pre_info = requests.post('https://api.fpt.ai/vision/idr/vnm', headers=headers, files=pre_img)
    behind_info = requests.post('https://api.fpt.ai/vision/idr/vnm', headers=headers, files=behind_img)

    info = {
        pre_info.json()['data'][0]['id']:{
            'name':pre_info.json()['data'][0]['name'],
            'dob':pre_info.json()['data'][0]['dob'],
            'sex':pre_info.json()['data'][0]['sex'],
            'nationality':pre_info.json()['data'][0]['nationality'],
            'home':pre_info.json()['data'][0]['home'],
            'address':pre_info.json()['data'][0]['address'],
            'features':behind_info.json()['data'][0]['features'],
            'issue_date':behind_info.json()['data'][0]['issue_date']
        }
    }
    return info


def save_img(id_card_font, id_card_back, face_image):
    id_card_font_path = os.path.join('flaskr/static/images', 'id_card_front_image.jpg')
    id_card_back_path = os.path.join('flaskr/static/images', 'id_card_back_image.jpg')
    face_image_path = os.path.join('flaskr/static/images', 'selfie_image.jpg')
    id_card_font.save(id_card_font_path)
    id_card_back.save(id_card_back_path)
    face_image.save(face_image_path)
    return (id_card_font_path,id_card_back_path,face_image_path)


def delete():
    for filename in os.listdir('flaskr/static/images'):
        os.remove(os.path.join('flaskr/static/images', filename))