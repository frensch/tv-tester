import compare_images

UPLOAD_FOLDER = './temp'
DB_FOLDER = './static/db'
TEST_IMG = './test_img'

#filename1 = UPLOAD_FOLDER + '/' + "Captura_de_Tela_2022-07-20_as_11.41.48.png"
#filename1 = UPLOAD_FOLDER + '/' + "IMG_20220727_210118.jpg"
#filename2 = DB_FOLDER + '/' + "Captura_de_Tela_2022-07-20_as_11.41.48.png"
#filename2 = DB_FOLDER + '/' + "Captura_de_Tela_2022-07-22_as_14.14.26.png"
filename1 = TEST_IMG + '/'+ 'home2.png'
filename2 = TEST_IMG + '/'+ 'home1.png'
image_ret = compare_images.findMatchByFiles(filename1, filename2)

print(image_ret)