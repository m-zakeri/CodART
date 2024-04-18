/*
 * Created on 27.03.2005
 */
package net.sourceforge.ganttproject.action;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;

import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.border.Border;
import javax.swing.border.EmptyBorder;

import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.calendar.WeekendCalendarImpl;
import net.sourceforge.ganttproject.document.Document;
import net.sourceforge.ganttproject.gui.UIFacade;
import net.sourceforge.ganttproject.gui.options.TopPanel;
import net.sourceforge.ganttproject.gui.projectwizard.I18N;
import net.sourceforge.ganttproject.gui.projectwizard.WeekendConfigurationPage;
import net.sourceforge.ganttproject.importer.ImporterFromGanttFile;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.language.GanttLanguage.Event;
import net.sourceforge.ganttproject.language.GanttLanguage.Listener;

/**
 * @author bard
 */
public class AddWeekendAction extends AbstractAction {
    private GanttProject myProject;
    private UIFacade myUIFacade;
    private Action myOkAction;
    private i18n myI18n;
    
    public AddWeekendAction(GanttProject project, UIFacade uiFacade) {
        super();
        myProject =project;
        myUIFacade = uiFacade;
        myI18n = new i18n();
        putValue(Action.NAME, myI18n.getButtonLabel());
    }
    public void actionPerformed(ActionEvent e) {
        final WeekendCalendarImpl calendar = new WeekendCalendarImpl();
        WeekendConfigurationPage weekendPage = new WeekendConfigurationPage(calendar, new I18N());
		JPanel component = new JPanel(new BorderLayout());
        component.setBorder(new EmptyBorder(0, 5, 0, 5));
		TopPanel topPanel = new TopPanel(weekendPage.getTitle(), null);
		JLabel warningLabel = new JLabel(myI18n.getWarningText());
		component.add(topPanel, BorderLayout.NORTH);
		component.add(weekendPage.getComponent(), BorderLayout.CENTER);
		component.add(warningLabel, BorderLayout.SOUTH);
        myOkAction =new OkAction() {
            public void actionPerformed(ActionEvent e) {
                
                Document document = myProject.getDocument();
                myProject.closeProject();
                for (int i=1; i<=7; i++) {
                    myProject.getActiveCalendar().setWeekDayType(i, calendar.getWeekDayType(i));                    
                }
                ImporterFromGanttFile importer = new ImporterFromGanttFile();
                importer.run(myProject, document);
                myProject.setDTDVersion("1.11");
                myProject.setHotAction(null);
            }
        };
        Action cancelAction = new CancelAction() {
            public void actionPerformed(ActionEvent e) {
            }
        };
        JDialog dialog= myUIFacade.createDialog(component, new Action[] {
                myOkAction, cancelAction
        });
    }
    
    private class i18n implements Listener {
        private i18n() {
            GanttLanguage.getInstance().addListener(this);
        }
        String getButtonLabel() {
            return GanttLanguage.getInstance().getText("projectWizard.weekend.magicButtonLabel");
        }
        String getWarningText() {
            return GanttLanguage.getInstance().getText("projectWizard.weekend.magicConverter.warningText");
        }
        public void languageChanged(Event event) {
            AddWeekendAction.this.putValue(Action.NAME, getButtonLabel());
        }
    }

}
