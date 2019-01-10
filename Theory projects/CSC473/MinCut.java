import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class MinCut{
	
	private class MultiGraph(){


		public MultiGraph(int n){
			//List<Pair<Integer>> edges = new ArrayList<>();

		}

	}

	public static void minCut(Graph g) {
		
		int n = g.adj.length;
		int [][] adj = new int[n][n];

		for (int i = 0; i < n; i++){
			for (int j = 0; j < n; j++){
				adj[i][j] = g.adj[i][j];
			}
		}

		List<Pair<Integer>> edges = new ArrayList<>();
		

		Random r = new Random();
		while (n-- > 2){
			int edge = r.nextInt(edges.size());
			contract(adj, edges.get(edge));


		}
		//Use disjoint sets to get cut
	}
	
	
	public static void contract(int [][] adj, int edge, List<Pair<Integer>> edges){
		
		int x = edges.get(edge).x; int y = edges.get(edge).y;
		x = Math.min(x,y); y = Math.max(x,y);

		for (int i = 0; i < adj.length; i++){
			adj[i][x] += adj[i][y];
			adj[x][i] += adj[y][i];
		}
		adj[x][x] = 0;
		
		Pair<Integer> e = edges.get(edge);
		while (edges.size() >= edge && edges.get(edge).equals(e)){
			edges.remove(edge);
		}

		while (0 < edges.size() && edges.get(--edge).equals(e)){
			edges.remove(edge);
		}

		
	}

	

	public static void main(String[] args) {

		

		
	}
	  
	
}
