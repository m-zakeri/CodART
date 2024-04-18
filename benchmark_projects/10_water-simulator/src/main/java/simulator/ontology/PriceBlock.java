package simulator.ontology;

import jade.content.Concept;

/** file: PriceBlock.java
 * @author ontology bean generator
 * @version 2003/08/12
 */


public class PriceBlock implements Concept{ 

  // Integer no
  private Integer no;
  public void setNo(Integer s) { this.no=s; }
  public Integer getNo() { return this.no; }

  // Integer limitDown
  private Integer limitDown;
  public void setLimitDown(Integer s) { this.limitDown=s; }
  public Integer getLimitDown() { return this.limitDown; }

  // Float price
  private Float price;
  public void setPrice(Float s) { this.price=s; }
  public Float getPrice() { return this.price; }

  // Integer limitUp
  private Integer limitUp;
  public void setLimitUp(Integer s) { this.limitUp=s; }
  public Integer getLimitUp() { return this.limitUp; }

}
