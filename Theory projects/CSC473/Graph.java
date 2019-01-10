
public class Graph{

	public int[][] adj;

	public Graph(int n){
		adj = new int[n][n];		
	}

	@Override
	public String toString(){
		return adj.toString();
	}	


	public void addEdge(int x, int y, int weight){
		adj[x][y] = weight;
	}
	   
}
