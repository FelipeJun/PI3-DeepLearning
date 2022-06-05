from ast import While
import discord
import uuid
from discord.ext import commands
# importing modules
import urllib.request
from PIL import Image
import numpy as np
import os
from keras.models import load_model

model = load_model('traffic_classifier.h5')

# Dicionario com os tipos de placa
classes = { 1:'Speed limit (20km/h)',
            2:'Speed limit (30km/h)', 
            3:'Speed limit (50km/h)', 
            4:'Speed limit (60km/h)', 
            5:'Speed limit (70km/h)', 
            6:'Speed limit (80km/h)', 
            7:'End of speed limit (80km/h)', 
            8:'Speed limit (100km/h)', 
            9:'Speed limit (120km/h)', 
            10:'No passing', 
            11:'No passing veh over 3.5 tons', 
            12:'Right-of-way at intersection', 
            13:'Priority road', 
            14:'Yield', 
            15:'Stop', 
            16:'No vehicles', 
            17:'Veh > 3.5 tons prohibited', 
            18:'No entry', 
            19:'General caution', 
            20:'Dangerous curve left', 
            21:'Dangerous curve right', 
            22:'Double curve', 
            23:'Bumpy road', 
            24:'Slippery road', 
            25:'Road narrows on the right', 
            26:'Road work', 
            27:'Traffic signals', 
            28:'Pedestrians', 
            29:'Children crossing', 
            30:'Bicycles crossing', 
            31:'Beware of ice/snow',
            32:'Wild animals crossing', 
            33:'End speed + passing limits', 
            34:'Turn right ahead', 
            35:'Turn left ahead', 
            36:'Ahead only', 
            37:'Go straight or right', 
            38:'Go straight or left', 
            39:'Keep right', 
            40:'Keep left', 
            41:'Roundabout mandatory', 
            42:'End of no passing', 
            43:'End no passing veh > 3.5 tons' }

bot = commands.Bot("")

@bot.event
async def on_ready():
  print(f"Estou pronto para uso {bot.user}")

#Comando para salvar imagens enviadas no chat na pasta do bot
# digitar no discord ("!salvar + anexo")
@bot.event
async def on_message(message):
    if message.author == bot.user:
     return

    if message.attachments:
        await message.channel.send(content=message.attachments[0].url)

    await bot.process_commands(message)
    
@bot.command(name = "placa")
async def save(ctx):
  try:
      imageName = str(uuid.uuid4()) + '.png'
      await ctx.message.attachments[0].save(imageName)
      file_path = os.getcwd()
      file_path = file_path + "\\"+imageName
      print(file_path)
      image = Image.open(file_path)
      image = image.resize((30,30))
      image = np.expand_dims(image, axis=0)
      image = np.array(image)
      y_prob = model.predict(image)
      sign=(np.argmax(y_prob,axis=1) + 1)
      placa = classes[int(sign)]
      print(placa)
      await ctx.send(placa)
  except:
    print("Error: Imagem não encontrada no Dataset")
    await ctx.send("Imagem não encontrada no Dataset")
  if os.path.isfile(file_path):
    os.remove(file_path)
    print("File has been deleted")
  else:
    print("File does not exist")
    
TOKEN = ("OTc3NjQ2NzE4NzM0NzAwNTc1.GsNMQ_.ayRNJeNy8B4WeGYFONAfYIMU2QGRvsL03x3up8")
bot.run(TOKEN)