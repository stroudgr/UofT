public class Pair<T> {

	    public T x,y;
	    
	    protected Pair(T x, T y){
	      this.x = x; this.y = y;
	    }
	    
	    public static <T> Pair<T> at(T x, T y){
	      return new Pair(x,y);
	    
	    }
	    
	    @Override
	    public String toString(){
	    	return "[ " + x.toString() + ", " + y.toString() + " ]";
	    }

	    @Override
	    public boolean equals(Object p){
	    	
	    	if (p == this)
	    		return true;
	    	
	    	if (!(p instanceof Pair)){
	    		return false;
	    	}
	    	
	    	Pair pp = (Pair <T>) p;
	    	
	    	return pp.x.equals(x) && pp.y.equals(y);
	    }
	    
	    @Override
	    public int hashCode(){
	    	return x.hashCode()*y.hashCode();
	    }
	    
	    
	  }