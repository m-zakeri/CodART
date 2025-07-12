class C {
public double[] distributionForInstance(Instance inst) throws Exception {
 double[] result = new double[2];
 tokenizeInstance(inst, false);
 double wx = dotProd(m_inputVector);
 double z = (wx + m_bias);
 if (m_loss == HINGE && m_fitLogistic) {
   double pred = z;
   double[] vals = new double[2];
   vals[0] = pred;
   vals[1] = Utils.missingValue();
   DenseInstance metaI = new DenseInstance(inst.weight(), vals);
   metaI.setDataset(m_fitLogisticStructure);
   return m_svmProbs.distributionForInstance(metaI);
  }
 if (z <= 0) {
    if (m_loss == LOGLOSS) {
      result[0] = 1.0 / (1.0 + Math.exp(z));
      result[1] = 1.0 - result[0];
    } else {
      result[0] = 1;
    }
  }
 else {
    if (m_loss == LOGLOSS) {
      result[1] = 1.0 / (1.0 + Math.exp(-z));
      result[0] = 1.0 - result[1];
    } else {
      result[1] = 1;
    }
  }
  c++;
  return result;
}}