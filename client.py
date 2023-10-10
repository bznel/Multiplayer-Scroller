import pygame, os, time, copy, socketio, json

sprites = {'idle': [], 'dead': [], 'jump': [], 'run': [], 'walk': []}

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
running = True
deltaTime = 0

for key in sprites:
  dir = "png/" + key + "/"

  for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    img = pygame.image.load(f)
    img = pygame.transform.scale(img, (100, 70))

    sprites[key].append(img)


def isFloat(string):
  try:
    float(string)
    return True
  except ValueError:
    return False


otherPlayers = []


class Player:
  position = pygame.Vector2()

  name = ""
  animation = "idle"
  facing = "right"

  animFrame = int(1)

  def __init__(self, position, name):
    self.position = position
    self.name = name

  def draw(self):
    spriteList = sprites[self.animation]

    if (isFloat(self.animFrame)):

      frame = int(self.animFrame / 4) - 1
      frameImage = spriteList[frame]

      if (self.facing == "left"):

        flippedImage = pygame.transform.flip(frameImage.copy(), True, False)

        adjusted_x = self.position.x - 65

        screen.blit(flippedImage, (adjusted_x, self.position.y))
      else:
        screen.blit(frameImage, self.position)

  def animate(self, animation):
    self.animation = animation


sio = socketio.Client()

sio.connect('http://game-server.vo1d.repl.co:80')


@sio.event
def player_data(data):
  positionData = json.loads(data['pos'])

  newVector = pygame.Vector2()
  newVector.x = positionData[0]
  newVector.y = positionData[1]

  found = False

  for player in otherPlayers:
    if player.name == data['sid']:
      found = True

  if found == False:
    newPlayer = Player(newVector, data['sid'])
    otherPlayers.append(newPlayer)
  else:
    for player in otherPlayers:
      if player.name == data['sid']:
        player.position = newVector
        player.facing = data['facing']
        player.animate(data['anim'])


@sio.event
def player_animation(data):
  animation = data['anim']

  for player in otherPlayers:
    if player.name == data['sid']:
      player.animate(animation)


class LocalPlayer:
  position = pygame.Vector2()

  name = ""
  animation = "idle"
  facing = "right"

  is_jumping = False
  on_ground = False
  heightLeftToJump = 0
  jump_speed = 10
  fall_speed = 5
  gravity = 1

  animFrame = int(1)

  def __init__(self, position, name):
    self.position = position
    self.name = name

  def draw(self):
    spriteList = sprites[self.animation]

    if self.is_jumping:  # for jumping
      self.heightLeftToJump -= self.jump_speed
      self.position.y -= self.jump_speed

      if self.heightLeftToJump <= 0:
        self.is_jumping = False
        self.on_ground = False

    if not self.on_ground:  # for falling
      self.fall_speed += self.gravity
      self.position.y += self.fall_speed

    self.on_ground = (self.position.y + 65 >= floor.position.y)

    if self.on_ground:  # keep them on the ground
      self.position.y = floor.position.y - 65
      self.is_jumping = False
      self.fall_speed = 0

    if (isFloat(self.animFrame)):

      frame = int(self.animFrame / 4) - 1
      animFrame = spriteList[frame]

      if (self.facing == "left"):

        flippedFrame = pygame.transform.flip(animFrame.copy(), True, False)

        adjusted_x = self.position.x - 65

        screen.blit(flippedFrame, (adjusted_x, self.position.y))
      else:
        screen.blit(animFrame, self.position)

      sio.emit(
          'update_player', {
              'pos': str(self.position),
              'anim': str(self.animation),
              'facing': str(self.facing),
          })

  def jump(self):
    if not self.is_jumping:
      self.is_jumping = True
      self.heightLeftToJump = 100

  def animate(self, animation):

    self.animation = animation

  def move(self, dir):
    self.animate("run")

    if (dir == "left"):
      self.facing = "left"
      self.position.x -= 300 * deltaTime

    elif dir == "right":
      self.facing = "right"
      self.position.x += 300 * deltaTime


class Floor:

  def __init__(self, position, width, height):
    self.position = position
    self.width = width
    self.height = height

  def draw(self):
    pygame.draw.rect(
        screen, (0, 255, 0),
        pygame.Rect(self.position.x, self.position.y, self.width, self.height))


localPlayer = LocalPlayer(
    pygame.Vector2(screen.get_width() / 2,
                   screen.get_height() / 2), "Test")

floor = Floor(pygame.Vector2(0,
                             screen.get_height() - 20), screen.get_width(), 20)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  screen.fill("purple")

  keys = pygame.key.get_pressed()

  idling = True

  if keys[pygame.K_a]:
    localPlayer.move("left")
    idling = False

  if keys[pygame.K_d]:
    localPlayer.move("right")
    idling = False

  if keys[pygame.K_SPACE]:
    localPlayer.jump()
    idling = False

  if (idling == True):
    localPlayer.animate("idle")

  for otherPlayer in otherPlayers:
    otherPlayer.animFrame = otherPlayer.animFrame + 1

    if otherPlayer.animFrame > 60:
      otherPlayer.animFrame = 1

    otherPlayer.draw()

  localPlayer.animFrame = localPlayer.animFrame + 1
  if localPlayer.animFrame > 60:
    localPlayer.animFrame = 1

  localPlayer.draw()
  floor.draw()

  pygame.display.flip()

  deltaTime = clock.tick(60) / 1000

pygame.quit()
