/*
 * Created on 10.11.2003
 *
 * To change the template for this generated file go to
 * Window>Preferences>Java>Code Generation>Code and Comments
 */
package org.gudy.azureus2.ui.common;

import org.gudy.azureus2.ui.common.IUserInterface;
import org.gudy.azureus2.ui.common.UITemplate;
import org.gudy.azureus2.ui.common.util.LGLogger2Log4j;

/**
 * @author tobi
 *
 * To change the template for this generated type comment go to
 * Window>Preferences>Java>Code Generation>Code and Comments
 */
public abstract class UITemplateHeadless
	extends UITemplate
	implements IUserInterface {

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.common.IUserInterface#init(boolean, boolean)
	 */
	public void init(boolean first, boolean others) {
		super.init(first, others);
		if (first)
			LGLogger2Log4j.set();

	}
}
