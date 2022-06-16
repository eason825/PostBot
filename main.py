# ill finish this later
#join discord.gg/fortnitedev

import os
os.system("python3 -m pip install py-cord==2.0.0rc1")

import discord
import requests
import json
from discord.ui import Button, View, InputText, Modal

bot = discord.Bot()


footertext = "Thanks For Using PostBot ❤" #embed footer text
color = 0xFFFFFF     #embed color (blurple)
cache = {}

class TypeDropdown(discord.ui.Select):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        options = [
            discord.SelectOption(label="GET", description="Send A GET Request"),
            discord.SelectOption(label="POST", description="Send A POST Request")
        ]
        super().__init__(
            placeholder="Select A Request Method...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        cache[str(interaction.user.id)]['method'] = f"{self.values[0]}"
        print(cache)
        view = finalView()
        embed = discord.Embed(title="Here is info for your request!", color=color)
        embed.add_field(name="URL:", value=f"{cache[str(interaction.user.id)]['website']}")
        embed.add_field(name="Method:", value=f"{self.values[0]}")
        embed.set_footer(text="If you would like to add on anything to this request, click the corresponding buttons!")
        await interaction.response.send_message(embed=embed, view=view)


class DropdownView(discord.ui.View):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        super().__init__()

        # Adds the dropdown to our View object
        self.add_item(TypeDropdown(self.bot))

class WebModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Send A Request!", placeholder="Input The Website You Would Like To Send A Request To"))

    async def callback(self, interaction: discord.Interaction):
      cache[str(interaction.user.id)] = {}
      cache[str(interaction.user.id)]['headers'] = "{}"
      cache[str(interaction.user.id)]['body'] = "{}"
      cache[str(interaction.user.id)]['embed'] = []
      cache[str(interaction.user.id)]['website'] = str(self.children[0].value)
      view = DropdownView(bot)
      embed = discord.Embed(title="Select a reqiest Method to begin sending a Request", color=color)
      embed.set_footer(text=footertext)
      await interaction.response.send_message(embed=embed, view=view)


class BodyModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Add A Body To The Request", placeholder="Make sure this is in Correct JSON Format"))

    async def callback(self, interaction: discord.Interaction):
      cache[str(interaction.user.id)]['body'] = f"{self.children[0].value}"
      cache[str(interaction.user.id)]['embed'].append(f"```Body | {self.children[0].value}```")
      view = finalView()
      
      embed = discord.Embed(title="Here is info for your request!", color=color)
      embed.add_field(name="URL:", value=f"{cache[str(interaction.user.id)]['website']}")
      embed.add_field(name="Method:", value=f"{cache[str(interaction.user.id)]['method']}")
      for item in cache[str(interaction.user.id)]['embed']:
        embed.add_field(name="Added:", value=f"{item}", inline=False)
      embed.set_footer(text="If you would like to add on anything to this request, click the corresponding buttons!")
      
      await interaction.response.edit_message(embed=embed, view=view)

class HeaderModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Add Headers To The Request", placeholder="Make sure this is in Correct JSON Format"))

    async def callback(self, interaction: discord.Interaction):
      cache[str(interaction.user.id)]['headers'] = f"{self.children[0].value}"
      cache[str(interaction.user.id)]['embed'].append(f"```Headers | {self.children[0].value}```")
      view = finalView()
      embed = discord.Embed(title="Here is info for your request!", color=color)
      embed.add_field(name="URL:", value=f"{cache[str(interaction.user.id)]['website']}")
      embed.add_field(name="Method:", value=f"{cache[str(interaction.user.id)]['method']}")
      for item in cache[str(interaction.user.id)]['embed']:
        embed.add_field(name="Added:", value=f"{item}", inline=False)
      embed.set_footer(text="If you would like to add on anything to this request, click the corresponding buttons!")
      await interaction.response.edit_message(embed=embed, view=view)




class finalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
      
    @discord.ui.button(
        label="Submit Request",
        style=discord.ButtonStyle.red,
        emoji="🔒",
        custom_id="submit"
    )
    async def create(self, button: discord.ui.Button, interaction: discord.Interaction):
      request = cache[str(interaction.user.id)]
      await interaction.response.defer()
      print(request)
      if request['method'] == "GET":
        r = requests.get(f"{request['website']}", headers=json.loads(request['headers']), json=request['body'])
      if request['method'] == "POST":
        r = requests.post(f"{request['website']}", headers=json.loads(request['headers']), json=request['body'])

      try:
        data = r.json()
        print(data)
      except:
        data = r.text
      with open(f"cache/{str(interaction.user.id)}.txt", "a") as f:
        f.write(str(data))
      embed = discord.Embed(title="Here is your requested content!", color=color)
      embed.set_footer(text=footertext)
      await interaction.followup.send(embed=embed, view=DisfinalView(), file=discord.File(f'cache/{str(interaction.user.id)}.txt'))
      os.remove(f'cache/{str(interaction.user.id)}.txt')

      
    @discord.ui.button(
        label="Add Body",
        style=discord.ButtonStyle.green,
        custom_id="submitbody"
    )
    async def bodey(self, button: discord.ui.Button, interaction: discord.Interaction):
      #do some task here idfk
      modal = BodyModal(title="Add A Body To The Request")
      await interaction.response.send_modal(modal)


  
    @discord.ui.button(
        label="Add Headers",
        style=discord.ButtonStyle.green,
        custom_id="submithead"
    )
    async def heder(self, button: discord.ui.Button, interaction: discord.Interaction):
      #do some task here idfk
      modal = HeaderModal(title="Add Headers To The Request")
      await interaction.response.send_modal(modal)

class DisfinalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
      
    @discord.ui.button(
        label="Submit Request",
        style=discord.ButtonStyle.red,
        emoji="🔒",
        custom_id="submit",
        disabled=True
    )
    async def create(self, button: discord.ui.Button, interaction: discord.Interaction):
      print()

      
    @discord.ui.button(
        label="Add Body",
        style=discord.ButtonStyle.green,
        custom_id="submitbody",
        disabled=True
    )
    async def bodey(self, button: discord.ui.Button, interaction: discord.Interaction):
      print()


  
    @discord.ui.button(
        label="Add Headers",
        style=discord.ButtonStyle.green,
        custom_id="submithead",
        disabled=True
    )
    async def heder(self, button: discord.ui.Button, interaction: discord.Interaction):
      print()


@bot.slash_command()
async def request(ctx):
  #view = DropdownView(bot)
  modal = WebModal(title="Send A Request")
  await ctx.send_modal(modal)
  #await ctx.respond("Select A Request Method To Begin!", view=view)

bot.run(os.environ['token'])
