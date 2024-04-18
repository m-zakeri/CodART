package net.sourceforge.ganttproject.chart;

import javax.swing.JTree;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreePath;
import java.util.ArrayList;
import java.util.List;
import java.util.Collections;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 */
public class VisibleNodesFilter {
    public List/*<Task>*/ getVisibleNodes(JTree jtree, int minHeight, int maxHeight, int nodeHeight) {
        List preorderedNodes = Collections.list(((DefaultMutableTreeNode)jtree.getModel().getRoot()).preorderEnumeration());
        List result = new ArrayList();
        int currentHeight = jtree.getRowHeight()/2;
        for (int i=1; i<preorderedNodes.size(); i++) {
            DefaultMutableTreeNode nextNode = (DefaultMutableTreeNode) preorderedNodes.get(i);
            if (currentHeight>=minHeight && jtree.isVisible(new TreePath(nextNode.getPath()))) {
                result.add(nextNode.getUserObject());
            }

            currentHeight+=jtree.getRowHeight();
        }
        return result;
    }

}
