
import numpy as np


class NeuralNetwork(object):                                                                 # Network Encapsulatoin
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):              # Main Method for execution
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights
        self.weights_input_to_hidden = np.random.normal(0.0, self.input_nodes**-0.5, 
                                       (self.input_nodes, self.hidden_nodes))

        self.weights_hidden_to_output = np.random.normal(0.0, self.hidden_nodes**-0.5, 
                                       (self.hidden_nodes, self.output_nodes))
        self.lr = learning_rate
        
        # sigmoid activatin function
        self.activation_function = lambda x : 1/(1 + np.exp(-x))              
  
                    

    def train(self, features, targets):
        ''' Train the network on batch of features and targets.
            features: 2D array, each row is one data record, each column is a feature
            targets: 1D array of target values
        
        '''
        n_records = features.shape[0]
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)

        for X, y in zip(features, targets):
            final_outputs, hidden_outputs = self.forward_pass_train(X)  
            delta_weights_i_h, delta_weights_h_o = self.backpropagation(final_outputs, hidden_outputs, X, y, 
                                                                        delta_weights_i_h, delta_weights_h_o)
        self.update_weights(delta_weights_i_h, delta_weights_h_o, n_records)


    def forward_pass_train(self, X):
        ''' Implement forward pass here 
            X: features batch

        '''
        ### Forward pass ###
        
        hidden_inputs = np.dot(X,self.weights_input_to_hidden)                  # signals into hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)                # signals from hidden layer

        final_inputs = np.dot(hidden_outputs,self.weights_hidden_to_output)     # signals into final output layer
        final_outputs = final_inputs                                            #signals from final output layer (f(x) = x)
        
        return final_outputs, hidden_outputs

        ### Backward pass ###
    def backpropagation(self, final_outputs, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):
        ''' Implement backpropagation
            final_outputs: output from forward pass
            y: target (i.e. label) batch
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers

        '''
        # Calculate Error.
        error = y-final_outputs 

        # Calculate the hidden layer's contribution to the error
        hidden_error = np.dot(error,self.weights_hidden_to_output.T)                              
        

        
        # Backpropagated output_error terms - Replace these values with your calculations.
        output_error_term = error                                               # acti. fun. = f(x) = x
        
              
        # Backpropagated hidden_error terms - Replace these values with your calculations.
        hidden_error_term = hidden_error * (hidden_outputs) * (1-hidden_outputs)
        
        ## Weight Change ## 
        delta_weights_i_h += hidden_error_term * X[:,None]                      # Weight step (input to hidden)
        delta_weights_h_o += output_error_term * hidden_outputs[:,None]         # Weight step (hidden to output)
        
        return delta_weights_i_h, delta_weights_h_o

    ### Weight Update ###
    def update_weights(self, delta_weights_i_h, delta_weights_h_o, n_records):
        ''' Update weights on gradient descent step
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers
            n_records: number of records

        '''
        self.weights_hidden_to_output += self.lr * delta_weights_h_o/n_records  # update hidden-to-output weights with gradient descent step
        self.weights_input_to_hidden += self.lr * delta_weights_i_h/n_records   # update input-to-hidden weights with gradient descent step


    ### For test Set (without back-propagation)
    def run(self, features):
        ''' Run a forward pass through the network with input features 
            features: 1D array of feature values
        '''  
        #### Forward Pass ####
        hidden_inputs = np.dot(features,self.weights_input_to_hidden)           # signals into hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)                # signals from hidden layer
        
        final_inputs = np.dot(hidden_outputs,self.weights_hidden_to_output)     # signals into final output layer
        final_outputs = final_inputs                                            # signals from final output layer
        
        return final_outputs
    
    
##### NOTE: Take Hyper Parameters to Main Notebook for ease #####
