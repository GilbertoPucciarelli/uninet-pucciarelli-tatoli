# UNINET: Modelo de Recomendaciones de Asignaturas para Estudiantes
 Authors: Nicolas Araque Volk - Gilberto Pucciarelli Mazzer - Vito Alessandro Tatoli Pedota
 
 Our work is based on the recommender system proposed by Araque, Rojas and Vitali in 2020. This research proposed a deep learning model based on recurrent neural networks that 
 can help every student to make better decisions about how many courses and in what combinations it is appropriate to enroll, in order to obtain better academic results. However, 
 the system relies only on the academic performance of the students of the System Engineering major from the Universidad Metropolitana. 
 
 Araque, Rojas and Vitali proposed a system that relies only on the academic performance of previous academic terms to predict the probability of passing all credits for the next
 period given a combination of courses to be registered. From this research, we establish as academic success the event of obtaining a passing grade in all the enrolled 
 courses for a given term. This definition of academic success is related to the successful fulfillment of the academic itinerary for the student to finish the career.
 
 Therefore, the objective of this research is to refine the recommendation system previously described by modifying the data preprocessing, architecture, and implementing an 
 embedding layer, allowing the deep learning model to escalate to all the careers dictated in the Universidad Metropolitana. This modification allows the recommendation 
 system to work for all the undergraduate careers of any university.

 ![Results Metrics](http://url/to/img.png)
 
 The results for this research are the following: we have achieved a binary accuracy of 72,78% and AUC (Area Under the Curve) of 79,79% for the validation dataset, compared
 to 76,78% and 82,80% respectively of Araque, Rojas and Vitali model.  
 
 ![Results Metrics](http://url/to/img.png) 
 
  We have successfully applied a convolutional recurrent neural network for academic performance prediction, refining the model previously proposed and using it 
  as a recommendation technique for next term course combination. As well as prior work on this task, we only used past academic performance (course grades) ordered 
  chronologically to predict next term academic success and we were able to develop a dense input vector representation for the historic academic terms with their respective 
  grades. 

  The modification of the architecture proposed by Araque et al. [2] into a ConvLSTM was a key component of the architecture to model how grades evolve from the first term of 
  the students to later ones, how this evolution influences the probability of success in the future terms and allowed the deep learning model to escalate to all the careers 
  dictated in the Universidad Metropolitana.
 
 # Files 
  Data Folder 
  - Contais different data files used for the development of the model. 
  
  Django App Folder 
  - Contains the web aplication used to test the recommender system. The model was made for the general use of the students of the Universidad Metropolitana. 
  
  Notebooks Folder - contains the notebooks used for the development of the model. 
  - The "Modelo UNINET.ipynb" file contains the neural network and the results obtained. 
  - The "Negative_Sampling_Solution-Copy1.ipynb" file contains the modification of the implementation proposed by Mikolov et al. of the Word2Vec Skip-Gram Model. 
  - The "Preprocesamiento de datos.ipynb" file contains the data-preprocessing. 
  . The "Graficos.ipynb" file contains the code to graph the behaviour of the data. 
  
 # References
 
 N. Araque, G. Rojas, and M. Vitali, “UniNet: Next Term Course Recommendation using Deep Learning,” arXiv.org, 2020. [Online]. Available: https://arxiv.org/abs/2009.09326
 
 T. Mikolov, K. Chen, G. Corrado, and J. Dean, “Efficient Estimation of Word Representations in Vector Space,” arXiv.org, 2013. [Online]. Available: https://arxiv.org/abs/1301.3781
