package net.sourceforge.ganttproject.action;

import java.awt.event.ActionEvent;

import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.Icon;
import javax.swing.ImageIcon;

public class NewArtefactAction extends GPAction implements RolloverAction {

	private ActiveActionProvider myProvider;
	private Icon myIconOnMouseOver;

	public NewArtefactAction(ActiveActionProvider provider, String iconSize) {
	    super("", iconSize);
		myProvider = provider;
	}
	public void actionPerformed(ActionEvent e) {
		AbstractAction activeAction = myProvider.getActiveAction();
		activeAction.actionPerformed(e);
	}
	
	public static interface ActiveActionProvider {
		public AbstractAction getActiveAction();
	}

    protected String getIconFilePrefix() {
        return "insert_";
    }


}
