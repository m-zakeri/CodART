package fi.vtt.noen.intellij;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.application.Application;
import com.intellij.openapi.application.ApplicationManager;

/**

 */
public class OBMAction extends AnAction {
  public void actionPerformed(AnActionEvent e) {
    Application application = ApplicationManager.getApplication();
    OBMApplicationComponent helloWorldComponent = application.getComponent(OBMApplicationComponent.class);
    helloWorldComponent.sayHello();
  }
}
