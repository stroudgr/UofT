import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Random;

public class ClosestPairs{

	public static <T> void shuffleArray(List<T> l){
	    
		Random r = new Random();
	    T temp;
	    int index;

	    for (int i = l.size() - 1; i > 0; i--){
	    	index = r.nextInt(i);
	    	temp = l.get(index);
	    	l.set(index, l.get(i));
	    	l.set(i, temp);
	    }


	  }

	  public static int dSimple(Pair<Integer> p, Pair<Integer> q){
		  return (p.x - q.x)*(p.x - q.x) + (p.y - q.y)*(p.y - q.y);
	  }
	  
	  
	  public static double d(Pair<Integer> p, Pair<Integer> q){
		  return Math.sqrt((p.x - q.x)*(p.x - q.x) + (p.y - q.y)*(p.y - q.y));
	  }

	private static class Point extends Pair<Integer>{
		
		
		public static Point at(Integer x, Integer y){
			return new Point(x, y);
		}
		public Point(Integer x, Integer y){
			super(x,y);
		}
	}

	protected static class Dictionary {

		private Map<Pair<Integer>, Point> map;
		private double delta;
		
		public Dictionary(double delta){
			map = new HashMap<>();
			this.delta = delta;
		}

		public void decreaseDelta(List<Point> p, int index, double delta){
			
			this.delta = delta;
			map.clear();

			for (int i = 0; i < index; i++){
				insert(p.get(i));
			}
		
		}
		public Pair<Integer> subsquare(Point p) {
			  
			  int s = (int) Math.floor(2*p.x/delta); 
			  int t = (int) Math.floor(2*p.y/delta);
			  
			  return Pair.at(s,t);
			  
		  }
		  
		public void insert(Point point){
			map.put(subsquare(point), point);
		}

		private Point closest(Point p) {
			
			//Finds the "subsquare" that point p is in 
			Pair<Integer> st = subsquare(p);
			
			Point closestToP = null;

			for (int i = -2; i <= 2; i++) {
				for (int j = -2; j <= 2; j++){
					
					Point q = map.get(Pair.at(st.x + i, st.y + j));
					
					if (q != null && d(p, q) < delta){
						closestToP = q;
						delta = d(p, q);
					}
				}
						
			}
			
			return closestToP;
		}
	
	}

	

	  public static void main(String[] args) {

		int n = 15;
		int N = 40;
		
		List<Point> pairs = new ArrayList<>();
		
		Random r = new Random();
		
		
	    for (int i = 0; i < n; i++) {
	    	int x = r.nextInt(N);
	    	int y = r.nextInt(N);
	    	pairs.add(Point.at(x,y));
	    	
	    }
		
		
	    System.out.println(pairs);
	    
	    closestPair(pairs);
	    
	  }
	  
	  public static Pair<Integer> subsquare(Pair<Integer> p, double delta) {
		  
		  int s = (int) Math.floor(2*p.x/delta); 
		  int t = (int) Math.floor(2*p.y/delta);
		  
		  return Pair.at(s,t);
		  
	  }
	  
	public static void insert(Map<Pair<Integer>,Pair<Integer>> map, Pair<Integer> p, double delta){
		map.put(subsquare(p, delta), p);
	}

	  
	public static void closestPair(List<Point> p){
		  
		// Randomly order the points
		shuffleArray(p);
		  
		// A dictionary to keep track of points examined thus far
		Dictionary dict = new Dictionary(d(p.get(0), p.get(1)));

		// The closest pair of points examined thus far.
		Pair<Point> cp = Pair.at(p.get(0), p.get(1));

		// The distance between the closest pair of points examined thus far.
		// double delta = d(cp.x, cp.y);
		  
		dict.insert(p.get(0));
		dict.insert(p.get(1));
		  
		for (int i = 2; i < p.size(); i++) {
			  
			// Returns the closest element in dictionary to the ith element of p. Returns null if all points in dictionary 
			//   are of distance greater than delta away from the ith element of p.
			Point q = dict.closest(p.get(i));

			if (q != null){
				// Updates closest pairs
				cp = Pair.at(p.get(i), q);
				double delta = d(cp.x, cp.y);
				
				// Updates all the old points with a new delta
				dict.decreaseDelta(p, i, delta);
				dict.insert(p.get(i));
				    
			} else {
				dict.insert(p.get(i));
			}
			  
		}
		 
		System.out.println("Closest pair is : " + cp);
		  
	}


	private static Pair<Integer> closest(Pair<Integer> p, Map<Pair<Integer>,Pair<Integer>> map, double delta) {
		
		//Finds the "subsquare" that point p is in 
		Pair<Integer> st = subsquare(p, delta);
		
		Pair<Integer> closestToP = null;

		for (int i = -2; i <= 2; i++) {
			for (int j = -2; j <= 2; j++){
				
				Pair<Integer> q = map.get(Pair.at(st.x + i, st.y + j));
				
				if (q != null && d(p, q) < delta){
					closestToP = q;
					delta = d(p, q);
				}
			}		
		}
		
		return closestToP;
	}
}
