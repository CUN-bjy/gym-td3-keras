# gym-td3-keras

Reference Code : [`gym-ddpg-keras`](https://github.com/CUN-bjy/gym-ddpg-keras)(DDPG)

Keras Implementation of TD3(Twin Delayed Deep Deterministic Policy Gradient) with PER(Prioritized Experience Replay) option on OpenAI gym framework

STATUS : [`IN PROGRESS`](https://github.com/CUN-bjy/gym-td3-keras/projects/1)

</br>

### [To do](https://github.com/CUN-bjy/gym-td3-keras/projects/1)

*What is differences from DDPG*

1. Overestimation Bias Problem Solved
   - [x] double Q-network 
   - [x] clipped double q-update

2. Addressing Variance
   - [x] delayed policy update
   - [x] target policy smoothing

*Training Test on Simulation*

- [ ] *RoboschoolInvertedPendulum-v1*
- [ ] *RoboschoolHopper-v1*
- [ ] *RoboschoolHalfCheetah-v1*
- [ ] *RoboschoolAnt-v1*

</br>

## Easy Installation

1. Make an independent environment using `virtualenv`

```bash
# install virtualenv module
sudo apt-get install python3-pip
sudo pip3 install virtualenv

# create a virtual environment named venv
virtualenv venv 

# activate the environment
source venv/bin/activate 
```

​	To escape the environment, `deactivate`

2. Install the requirements

```bash
pip install -r requirements.txt
```

3. Run the training node

```python
#trainnig
python train.py
```

</br>

## Reference

[1] Addressing Function Approximation Error in Actor-Critic Methods

```
@misc{fujimoto2018addressing,
      title={Addressing Function Approximation Error in Actor-Critic Methods}, 
      author={Scott Fujimoto and Herke van Hoof and David Meger},
      year={2018},
      eprint={1802.09477},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```

[`REVIEW`](https://github.com/CUN-bjy/rl-paper-review/blob/master/reviews/TD3.md)	|	[`PAPER`](https://arxiv.org/pdf/1802.09477.pdf)

[2] [CUN-bjy/gym-ddpg-keras](https://github.com/CUN-bjy/gym-ddpg-keras)

[3] [sfujim/TD3](https://github.com/sfujim/TD3)

[4] [quantumiracle/SOTA-RL-Algorithms](https://github.com/quantumiracle/SOTA-RL-Algorithms)