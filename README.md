# gym-td3-keras

Reference Code : [`gym-ddpg-keras`](https://github.com/CUN-bjy/gym-ddpg-keras)(DDPG)

Keras Implementation of TD3(Twin Delayed Deep Deterministic Policy Gradient) with PER(Prioritized Experience Replay) option on OpenAI gym framework

STATUS : [`IN PROGRESS`](https://github.com/CUN-bjy/gym-td3-keras/projects/1)

This branch is just for debugging, **change the branch to main**.

</br>

### [To do](https://github.com/CUN-bjy/gym-td3-keras/projects/1)

*Test on Simulation*

- [ ] *RoboschoolInvertedPendulum-v1*
- [ ] *RoboschoolHopper-v1*
- [ ] *RoboschoolHalfCheetah-v1*
- [ ] *RoboschoolAnt-v1*

</br>

## Experiment Details from paper

**Network Model & Hyperparameter**

- For our implementation of DDPG, we use a two layer feedforward neural network of **400 and 300 hidden nodes** respectively, with rectified linear units (**ReLU**) between each layer for both the actor and critic, and a final **tanh** unit following the output of the actor.
- Unlike the original DDPG, the critic receives **both the state and action as input to the first layer**.
- Both network parameters are updated using **Adam** with a **learning rate of 10−3**.
- After each time step, the networks are trained with a **mini-batch of a 100 transitions**, **sampled uniformly** from a replay buffer containing the entire history of the agent.
- Both target networks are updated with **τ = 0.005**.

**Differences from DDPG**

- The target policy smoothing is implemented by **adding ![img](https://latex.codecogs.com/gif.latex?%5Cepsilon%20%5Csim%20%5Cmathcal%7BN%7D%280%2C0.2%29)** **to the actions** chosen by the target actor network, **clipped to (−0.5, 0.5)**.

- Delayed policy updates consists of only **updating the actor and target critic network** **every d iterations**, with d = 2.

  (While a larger d would result in a larger benefit with respect to accumulating errors, for fair comparison, the critics are only trained once per time step, and training the actor for too few iterations would cripple learning.)

**Exploration**

- To remove the dependency on the initial parameters of the policy we use a **purely exploratory policy for the** **first 10000 time steps** of stable length environments.

- Afterwards, we use an **off-policy exploration strategy**, <u>adding Gaussian noise N (0, 0.1) to each action</u>.

  (we found noise drawn from the Ornstein-Uhlenbeck process offered no performance benefits.)

**Evaluation**

- Each task is run for 1 million time steps with **evaluations every 5000 time steps**, where each evaluation reports the average reward over 10 episodes **with no exploration noise**.

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
