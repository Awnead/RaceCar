import argparse
import sys
import numpy as np
from PIL import Image
import gym
from gym import wrappers, logger

class CarController():
    def __init__(self):
        self.a = np.array([0.0,0.0,0.0])
        self.b = ["Left,Up,Right,Up"]

    def Left(self):
        self.a[0] += -0.1
    
    def Right(self):
        self.a[0] += 0.1
    
    def Up(self):
        self.a[1] += 0.2
    
    def Down(self):
        self.a[2] += 0.2
    
    def Clear(self):
        self.a = np.array([0.0,0.0,0.0])

class RandomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space
        self.car = CarController()

    def act(self, observation, reward, done):
        self.car.Clear()
        observation[60][47] = ( 0, 0, 0)
        observation[30][47] = ( 0, 0, 0)
        observation[1][43],observation[1][45],observation[1][47]=(0,0,0)
        im = Image.fromarray(observation)
        im.save("img15_45.png")
        self.speedControl(observation)
        print(self.car.a)
        return self.car.a

    def speedControl(self, observation): 
        row = [observation[0][43],observation[0][44],observation[0][45],observation[0][47],observation[0][48]]
        if tuple(row[1]) != ( 107, 107, 107 ) and tuple(row[-2]) != ( 107, 107, 107):
            #self.car.Down()
            print("speedControl observed off road")
        else:
            self.car.Up()
            print("speedControl observed on road")
        if tuple(row[2]) != ( 107, 107, 107):
            if tuple(observation[30][45]) != (107,107,107) and tuple(observation[60][45]) != (107,107,107):
                print("speedControl observed road curve")
                self.curveControl(observation)
            else:
                self.car.Up()
                print("speedControl observed straight road")

    def curveControl(self,observation):
        row = [observation[60][43],observation[60][44],observation[60][45],observation[60][47],observation[60][48]]
        if tuple(row[0]) != ( 107, 107, 107 ) and tuple(row[-1]) != ( 107, 107, 107):
            #self.car.Down()
            print("curveControl observed off road")
        else:
            self.car.Up()
            print("curveControl observed on road")
        if tuple(row[2]) != ( 107, 107, 107):
            if tuple(observation[60][45]) != (107,107,107):
                #ToDo:
                print("curveControl observed road curve")
            else:
                self.car.Up()
                print("curveControl observed straight road")
        if tuple(row[1]) != ( 107, 107, 107):
            self.car.Right()
            if tuple(row[1]) != (107,107,107):
                self.car.Right()
        elif tuple(row[-2]) != (107,107,107):
            self.car.Left()
            if tuple(row[-2]) != (107,107,107):
                self.car.Left()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('env_id', nargs='?', default='CarRacing-v0', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    #outdir = '/tmp/random-agent-results'
    #env = wrappers.Monitor(env, directory=outdir, force=True)
    env.seed(0)
    agent = RandomAgent(env.action_space)

    episode_count = 1
    reward = 0
    done = False

    for i in range(episode_count):
        ob = env.reset()
        while True:
            env.render()
            action = agent.act(ob, reward, done)
            ob, reward, done, _ = env.step(action)
            if done:
                break
            # Note there's no env.render() here. But the environment still can open window and
            # render if asked by env.monitor: it calls env.render('rgb_array') to record video.
            # Video is not recorded every episode, see capped_cubic_video_schedule for details.

    # Close the env and write monitor result info to disk
    env.close()
