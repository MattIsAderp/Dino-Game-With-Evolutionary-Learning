# Sprites from https://www.spriters-resource.com/pc_computer/trexgame/sheet/78171/ (for if we ever need any more of them)
from lib.Ground import Ground
from lib.Cactus import Cactus
from lib.Bird import Bird
from lib.Dino import Dinosaur
from lib.config import *

#random.seed(69420)

tick = 0
obst = 0
test = 0

def sigmoid(z):
    return 1./(1+np.exp(-z))


class Brain:
    def __init__(self, nn):
        if type(nn) != type(None):
            self.nn = nn
        else:
            self.nn = [np.random.uniform(-5, 5, (4,2)),
                       np.random.uniform(-5, 5, (3,2))]
        self.body = Dinosaur(START_POS, 600)
        self.fitness = 0
        self.score = 0
        self.moves = 0


class Population:
    POP_SIZE = POPULATION_SIZE

    def __init__(self):
        self.dinos = self.POP_SIZE
        self.generation = []
        self.BestEver = [None, 0]
        for i in range(self.POP_SIZE):
            self.generation.append(Brain(None))

    def generate(self):
        self.calculateFitness()
        self.savedGeneration = self.generation
        self.generation = []

        bestBrain = None
        for brain in self.savedGeneration:
            if bestBrain != None:
                if brain.fitness > bestBrain.fitness:
                    bestBrain = brain
            else:
                bestBrain = brain

        if bestBrain.score > self.BestEver[1]:
            self.BestEver[0] = copy.deepcopy(bestBrain.nn)
            self.BestEver[1] = bestBrain.score


        self.generation.append(Brain(bestBrain.nn))
        self.generation.append(Brain(copy.deepcopy(self.BestEver[0])))

        for i in range(20):
            self.generation.append(Brain(None))

        for i in range(self.POP_SIZE-22):
            brain = self.pickOne()
            self.generation.append(brain)

        self.dinos = len(self.generation)

    def move(self, inputs):
        for brain in self.generation:
            if brain.body != None:
                acInputs = np.vstack([1, inputs])
                #print(acInputs)

                theta_1 = brain.nn[0]
                theta_2 = brain.nn[1]

                a_1 = sigmoid(np.dot(acInputs.transpose(), theta_1)).transpose()
                a_1 = np.vstack([1, a_1])
                outputs = sigmoid(np.dot(a_1.transpose(), theta_2))

                output_i = np.argmax(outputs)
                output = -1

                if outputs[0][output_i] > 0.5:
                    output = output_i

                if output == 0:
                    brain.body.jump()
                    brain.moves += 1

                if output == 1 and brain.body.ducking != True:
                    brain.body.duck(True)
                    brain.moves += 1

                if output != 1 and brain.body.ducking != False:
                    brain.body.duck(False)

                brain.score += 1

                brain.body.move()

    def calculateFitness(self):
        totalScore = 0
        for brain in self.generation:
            totalScore += brain.score

        for brain in self.generation:
            brain.fitness = brain.score / totalScore
        wks.append_row([totalScore])


    def fitnessPick(self):
        index = 0
        r = np.random.uniform(0, 1)

        while r > 0:
            r = r - self.savedGeneration[index].fitness
            index += 1
        index -= 1

        nn = self.savedGeneration[index].nn
        return nn

    def pickOne(self):
        nn_1 = self.fitnessPick()
        nn_2 = self.fitnessPick()

        nn = self.crossover(nn_1, nn_2, 0.2)
        nn = self.mutate(nn_1, 0.1)

        brain = Brain(nn)

        return brain

    def crossover(self, nn_1, nn_2, rate):
        if np.random.uniform(0, 1) < rate:
            k = -1
            for layer in nn_1:
                k += 1
                j = -1
                for row in layer:
                    j += 1
                    i = -1
                    for weight in row:
                        i += 1
                        if np.random.uniform(0, 1) <= 0.8:
                            nn_1[k][j][i] = nn_2[k][j][i]
        return nn_1


    def mutate(self, nn, rate):
        for layer in nn:
            for weight in np.nditer(layer, op_flags=['readwrite']):
                if np.random.uniform(0, 1) < rate:
                    val = np.random.uniform(-5, 5)
                    weight[...] += val
                    if weight[...] > 5:
                        weight[...] = 5
                    elif weight[...] < -5:
                        weight[...] = -5

        return nn

    def collide(self, obstacle):
        for brain in self.generation:
            if brain.body != None:
                if obstacle.collide(brain.body):     # Dino collided with an obstacle, it lost
                    brain.body = None
                    self.dinos -= 1


    def draw(self, win):
        for brain in self.generation:
            if brain.body != None:
                brain.body.draw(win)


def draw_window(win, population, obstacles, ground, score, gen, inputs, closestObstacle):
    win.fill((255, 255, 255))     # Clear the screen

    for obstacle in obstacles:    # Draw every cactus
        obstacle.draw(win)

    gen_text = GEN_FONT.render("Generation " + str(gen), 1, (0, 0, 0))
    win.blit(gen_text, (WIN_WIDTH - 230, 50))

    score_text = SCORE_FONT.render("Score: " + str(round(score)), 1, (100, 100, 100))
    win.blit(score_text, (WIN_WIDTH - 170, 80))

    dino_amount_text = SCORE_FONT.render("Dinos: " + str(population.dinos), 1, (100, 100, 100))
    win.blit(dino_amount_text, (WIN_WIDTH - 170, 100))

    input1_text = INPUT_FONT.render("Dist: " + str(inputs[0]), 1, (255, 0, 0))
    #input2_text = INPUT_FONT.render("Top: " + str(inputs[1]), 1, (0, 255, 0))
    #input3_text = INPUT_FONT.render("Bot: " + str(inputs[2]), 1, (0, 0, 255))
    input2_text = INPUT_FONT.render("Bird: " + str(inputs[1]), 1, (255, 128, 128))
    input3_text = INPUT_FONT.render("Spd: " + str(inputs[2]), 1, (0, 128, 255))
    win.blit(input1_text, (50, 50))
    win.blit(input2_text, (50, 70))
    win.blit(input3_text, (50, 90))
    #win.blit(input4_text, (50, 110))
    #win.blit(input5_text, (50, 130))

    if closestObstacle != None:
        pygame.draw.line(win, (255, 0, 0), (closestObstacle.x, 0), (closestObstacle.x, WIN_HEIGHT), 2)

    ground.draw(win)     # Draw the ground
    population.draw(win)     # Draw the dino
    pygame.display.update()     # Update the display


def main():
    global tick
    global test
    global level_speed
    global obst
    population = Population()
    ground = Ground()
    obstacles = []
    inputs = np.zeros((3, 1))
    gen = 1
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    #wks.delete_col(1)

    score = 0
    ticks_until_obstacle = 50

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)     # Set the game at a frame rate of x FPS
        level_speed += LEVEL_SPEED_ACCEL
        if level_speed > MAX_LEVEL_SPEED:
            level_speed = MAX_LEVEL_SPEED

        tick += 1
        test += 1

        for event in pygame.event.get():    # If the window is closed, stop running the main loop
           if event.type == pygame.QUIT:
               run = False

        rem = []    # List of obstacles to remove
        closestObstacle = None
        for obstacle in obstacles:
            population.collide(obstacle)

            if obstacle.x + obstacle.img.get_width() < 0:    # Check if the obstacle is out of the screen
                rem.append(obstacle)     # Add the obstacle to the list of obstacles to remove

            if closestObstacle != None and closestObstacle.x + closestObstacle.img.get_width() < 150:
                closestObstacle = None

            if closestObstacle != None:
                if obstacle.x >= 150 and obstacle.x < closestObstacle.x:
                    closestObstacle = obstacle
            else:
                closestObstacle = obstacle

            obstacle.move(level_speed)

        for obstacle in rem:     # Remove every obstacle in rem
            obstacles.remove(obstacle)

        if tick % ticks_until_obstacle == 0:
            obst += 1
            if obst % 2 == 1:
                obstacles.append(Cactus(WIN_WIDTH))
            else:
                obstacles.append(Bird(WIN_WIDTH))

            #if random.randint(1,2) == 1:
            #    obstacles.append(Cactus(WIN_WIDTH))
            #else:
            #    #obstacles.append(Cactus(WIN_WIDTH))
            #    obstacles.append(Bird(WIN_WIDTH))

            ticks_until_obstacle = random.randint(35,45)
            tick = 0


        ground.move(level_speed)
        if population.dinos > 0:
            population.move(inputs)
        else:
            #random.seed(69420)
            inputs = np.zeros((3, 1))
            obstacles = []
            ground = Ground()
            score = 0
            gen += 1
            level_speed = START_LEVEL_SPEED
            population.generate()


        score += 1     # Up the score every frame

        if closestObstacle != None:
            inputs[0] = (closestObstacle.x)/WIN_WIDTH
            #inputs[1] = 0#(closestObstacle.y)/WIN_HEIGHT

            if type(closestObstacle) == type(Bird(0)):
                inputs[1] = ((463 - closestObstacle.y + closestObstacle.img.get_height())/WIN_HEIGHT) * 10
                if inputs[1] < 0:
                    inputs[1] = -1
            else:
                inputs[1] = -1

        inputs[2] = (level_speed)/MAX_LEVEL_SPEED

        draw_window(win, population, obstacles, ground, score, gen, inputs, closestObstacle)


    pygame.quit()    # Terminate the game
    quit()     # Terminate the script

main()
