function [C, sigma] = dataset3Params(X, y, Xval, yval)
%DATASET3PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = DATASET3PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
% C = 1;
% sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%


testValues = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30];

for i=1:length(testValues), % Test all possible values for C
    for j=1:length(testValues), % Test for sigma

	% Use the svmTrain function to get model output for each
	% possible combination of i, j (C, sigma)
        kernelFunction = @(x1, x2) gaussianKernel(x1, x2, testValues(j));
	testModel = svmTrain(X, y, testValues(i), kernelFunction);

	% Get the prediction vectors
	testPredictions = svmPredict(testModel, Xval);

	% Calculate the prediction error as indicated in the instructions
	crossValPredictErrors(i, j) = mean(double(testPredictions ~= yval));

    end;
end;

% Find the minimum value and index in the crossValPredictErrors matrix
[minColumnError, minColumnErrorIndex] = min(crossValPredictErrors);
[minError, minErrorIndex] = min(minColumnError);

% Select the optimal C and sigma using those indexes on the testValues vector
C = testValues(minColumnErrorIndex(minErrorIndex));
sigma = testValues(minErrorIndex);


% =========================================================================

end
