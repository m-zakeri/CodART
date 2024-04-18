package fi.vtt.noen.intellij;

import edu.uci.ics.jung.algorithms.layout.FRLayout;
import edu.uci.ics.jung.graph.Graph;
import edu.uci.ics.jung.graph.util.TestGraphs;
import edu.uci.ics.jung.visualization.DefaultVisualizationModel;
import edu.uci.ics.jung.visualization.GraphZoomScrollPane;
import edu.uci.ics.jung.visualization.RenderContext;
import edu.uci.ics.jung.visualization.VisualizationModel;
import edu.uci.ics.jung.visualization.VisualizationServer;
import edu.uci.ics.jung.visualization.annotations.AnnotatingGraphMousePlugin;
import edu.uci.ics.jung.visualization.annotations.AnnotatingModalGraphMouse;
import edu.uci.ics.jung.visualization.annotations.AnnotationControls;
import edu.uci.ics.jung.visualization.control.CrossoverScalingControl;
import edu.uci.ics.jung.visualization.control.ModalGraphMouse;
import edu.uci.ics.jung.visualization.control.ScalingControl;
import edu.uci.ics.jung.visualization.decorators.PickableEdgePaintTransformer;
import edu.uci.ics.jung.visualization.decorators.PickableVertexPaintTransformer;
import edu.uci.ics.jung.visualization.decorators.ToStringLabeller;
import edu.uci.ics.jung.visualization.renderers.Renderer;
import edu.uci.ics.jung.visualization.VisualizationViewer;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**

 */
public class JungTesting extends JFrame {
  JDialog helpDialog;
  VisualizationServer.Paintable viewGrid;

  public JungTesting() {
    Graph<String, Number> graph = TestGraphs.getOneComponentGraph();

    // the preferred sizes for the two views
    Dimension preferredSize1 = new Dimension(600,600);

    // create one layout for the graph
    FRLayout<String,Number> layout = new FRLayout<String,Number>(graph);
    layout.setMaxIterations(500);

    VisualizationModel<String,Number> vm =
        new DefaultVisualizationModel<String,Number>(layout, preferredSize1);

    // create 2 views that share the same model
    final VisualizationViewer<String,Number> vv =
        new VisualizationViewer<String,Number>(vm, preferredSize1);
    vv.setBackground(Color.white);
    vv.getRenderContext().setEdgeDrawPaintTransformer(new PickableEdgePaintTransformer<Number>(vv.getPickedEdgeState(), Color.black, Color.cyan));
    vv.getRenderContext().setVertexFillPaintTransformer(new PickableVertexPaintTransformer<String>(vv.getPickedVertexState(), Color.red, Color.yellow));
    vv.getRenderContext().setVertexLabelTransformer(new ToStringLabeller<String>());
    vv.getRenderer().getVertexLabelRenderer().setPosition(Renderer.VertexLabel.Position.CNTR);

    // add default listener for ToolTips
    vv.setVertexToolTipTransformer(new ToStringLabeller<String>());

//        ToolTipManager.sharedInstance().setDismissDelay(10000);

    Container content = getContentPane();
    Container panel = new JPanel(new BorderLayout());

    GraphZoomScrollPane gzsp = new GraphZoomScrollPane(vv);
    panel.add(gzsp);

    helpDialog = new JDialog();
    helpDialog.getContentPane().add(new JLabel("tesktiä"));

    RenderContext<String,Number> rc = vv.getRenderContext();
    AnnotatingGraphMousePlugin<String,Number> annotatingPlugin =
        new AnnotatingGraphMousePlugin<String,Number>(rc);
    // create a GraphMouse for the main view
    //
    final AnnotatingModalGraphMouse<String,Number> graphMouse =
        new AnnotatingModalGraphMouse<String,Number>(rc, annotatingPlugin);
    vv.setGraphMouse(graphMouse);
    vv.addKeyListener(graphMouse.getModeKeyListener());

    final ScalingControl scaler = new CrossoverScalingControl();

    JButton plus = new JButton("+");
    plus.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
            scaler.scale(vv, 1.1f, vv.getCenter());
        }
    });
    JButton minus = new JButton("-");
    minus.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
            scaler.scale(vv, 1/1.1f, vv.getCenter());
        }
    });

    JComboBox modeBox = graphMouse.getModeComboBox();
    modeBox.setSelectedItem(ModalGraphMouse.Mode.ANNOTATING);

    JButton help = new JButton("Help");
    help.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
            helpDialog.pack();
            helpDialog.setVisible(true);
        }
    });

    JPanel controls = new JPanel();
    JPanel zoomControls = new JPanel();
    zoomControls.setBorder(BorderFactory.createTitledBorder("Zoom"));
    zoomControls.add(plus);
    zoomControls.add(minus);
    controls.add(zoomControls);

    JPanel modeControls = new JPanel();
    modeControls.setBorder(BorderFactory.createTitledBorder("Mouse Mode"));
    modeControls.add(graphMouse.getModeComboBox());
    controls.add(modeControls);

    JPanel annotationControlPanel = new JPanel();
    annotationControlPanel.setBorder(BorderFactory.createTitledBorder("Annotation Controls"));

    AnnotationControls<String,Number> annotationControls =
        new AnnotationControls<String,Number>(annotatingPlugin);

    annotationControlPanel.add(annotationControls.getAnnotationsToolBar());
    controls.add(annotationControlPanel);

    JPanel helpControls = new JPanel();
    helpControls.setBorder(BorderFactory.createTitledBorder("Help"));
    helpControls.add(help);
    controls.add(helpControls);
    content.add(panel);
    content.add(controls, BorderLayout.SOUTH);
  }

  public static void main(String[] args) {
    JFrame f = new JungTesting();
    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
//    f.getContentPane().add(new JungTesting());
    f.pack();
    f.setVisible(true);
  }
}
