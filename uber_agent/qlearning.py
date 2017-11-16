




def getDistance():


def featureExtractor(state, action):
    src, dest = action
    defaultVal = 1
    features = {}
    # distance state -> src, src -> dest
    features['dist1'] = getDistance(state, src)
    features['dist2'] = getDistance(src, dest)
    # location itself
    features['cur_' + state] = defaultVal
    features['src_'+src] = defaultVal
    features['dest_'+dest] = defaultVal
    return features

def getQ(state, action):
    score = 0
    for f, v in featureExtractor(state, action).iteritems():
        score += self.weight[f] * v
    return score

def backward(state, action, reward, newState):
    # if newState == None:
    #     # in terminal state
    #     vNewState = 0
    # else:
        # newAction = max((self.getQ(newState, a), a) for a in self.actions(newState))[1]
        # vNewState = self.getQ(newState, newAction)
    x = self.getStepSize() * (self.getQ(state, action) - reward )
    for f,v in self.featureExtractor(state, action):
        self.weights[f] = self.weights.get(f) - x * v



