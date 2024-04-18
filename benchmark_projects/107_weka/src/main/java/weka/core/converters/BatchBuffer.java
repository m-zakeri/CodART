package weka.core.converters;

import weka.core.Instance;
import weka.core.Instances;

import java.io.File;
import java.io.Serializable;
import java.net.URL;

public class BatchBuffer implements Serializable {
    /**
     * the loader.
     */
    private Loader m_Loader;
    /**
     * whether the loader is incremental.
     */
    private boolean m_Incremental;
    /**
     * the instance counter for the batch case.
     */
    private int m_BatchCounter;
    /**
     * the last internally read instance.
     */
    private Instance m_IncrementalBuffer;
    /**
     * the batch buffer.
     */
    private Instances m_BatchBuffer;

    public Loader getM_Loader() {
        return m_Loader;
    }

    public void setM_Loader(Loader m_Loader) {
        this.m_Loader = m_Loader;
    }

    public boolean getM_Incremental() {
        return m_Incremental;
    }

    public void setM_Incremental(boolean m_Incremental) {
        this.m_Incremental = m_Incremental;
    }

    public void setM_BatchBuffer(Instances m_BatchBuffer) {
        this.m_BatchBuffer = m_BatchBuffer;
    }

    /**
     * initializes the batch buffer if necessary, i.e., for non-incremental
     * loaders.
     */
    public void initBatchBuffer() {
        try {
            if (!m_Incremental)
                m_BatchBuffer = m_Loader.getDataSet();
            else
                m_BatchBuffer = null;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * resets the loader.
     *
     * @throws Exception if resetting fails
     */
    public void reset(File thisM_File, URL thisM_URL) throws Exception {
        if (thisM_File != null)
            ((AbstractFileLoader) m_Loader).setFile(thisM_File);
        else if (thisM_URL != null)
            ((URLSourcedLoader) m_Loader).setURL(thisM_URL.toString());
        else if (m_Loader != null)
            m_Loader.reset();

        m_BatchCounter = 0;
        m_IncrementalBuffer = null;

        if (m_Loader != null) {
            if (!m_Incremental)
                m_BatchBuffer = m_Loader.getDataSet();
            else
                m_BatchBuffer = null;
        }
    }

    /**
     * returns whether there are more Instance objects in the data.
     *
     * @param structure the structure of the dataset
     * @return true if there are more Instance objects
     * available
     * @see        #nextElement(Instances)
     */
    public boolean hasMoreElements(Instances structure) {
        boolean result;

        result = false;

        if (m_Incremental) {
            // user still hasn't collected the last one?
            if (m_IncrementalBuffer != null) {
                result = true;
            } else {
                try {
                    m_IncrementalBuffer = m_Loader.getNextInstance(structure);
                    result = (m_IncrementalBuffer != null);
                } catch (Exception e) {
                    e.printStackTrace();
                    result = false;
                }
            }
        } else {
            result = (m_BatchCounter < m_BatchBuffer.numInstances());
        }

        return result;
    }

    /**
     * returns the next element and sets the specified dataset, null if
     * none available.
     *
     * @param dataset the dataset to set for the instance
     * @return the next Instance
     */
    public Instance nextElement(Instances dataset) {
        Instance result;

        result = null;

        if (m_Incremental) {
            // is there still an instance in the buffer?
            if (m_IncrementalBuffer != null) {
                result = m_IncrementalBuffer;
                m_IncrementalBuffer = null;
            } else {
                try {
                    result = m_Loader.getNextInstance(dataset);
                } catch (Exception e) {
                    e.printStackTrace();
                    result = null;
                }
            }
        } else {
            if (m_BatchCounter < m_BatchBuffer.numInstances()) {
                result = m_BatchBuffer.instance(m_BatchCounter);
                m_BatchCounter++;
            }
        }

        if (result != null) {
            result.setDataset(dataset);
        }

        return result;
    }

    /**
     * returns the structure of the data.
     *
     * @throws Exception if something goes wrong
     * @return the structure of the data
     */
    public Instances getStructure() throws Exception {
        if (m_BatchBuffer == null)
            return m_Loader.getStructure();
        else
            return new Instances(m_BatchBuffer, 0);
    }

    /**
     * returns the full dataset, can be null in case of an error.
     *
     * @throws Exception if resetting of loader fails
     * @return the full dataset
     */
    public Instances getDataSet(File thisM_File, URL thisM_URL) throws Exception {
        Instances result;

        result = null;

        // reset the loader
        reset(thisM_File, thisM_URL);

        try {
            if (m_BatchBuffer == null)
                result = m_Loader.getDataSet();
            else
                result = m_BatchBuffer;
        } catch (Exception e) {
            e.printStackTrace();
            result = null;
        }

        return result;
    }
}