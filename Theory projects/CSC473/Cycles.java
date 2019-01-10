import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class Cycles{
	
	
	public static boolean triangle(Graph g){

		int addSqaured[][] = Matrix.multiply(g.adj, g.adj);
		for (int i = 0; i < g.adj.length; i++){
			for (int j = 0; j < g.adj.length; j++){
				if (addSqaured[i][j] && g.adj[j][i]){
					return true;
				}
			}
		}
	}

	public static Map<Pair<Integer>, Integer> getTriangles(Graph g){
		Map<Pair<Integer>, Integer> triangles = new HashMap<>();
		
		//TODO use Boolean product witness matrix

		return triangles;
	}

	// For a specific permutation where the pi values are the corresponding index in the adjacency matrix.
	public static boolean piIncreasingKCycle(Graph g, int k){

		int adj[][] = new int[][];
		for (int i = 0; i < g.adj.length; i++){
			for (int j = i; j < g.adj.lenghth; j++){
				adj[i][j] = g.adj[i][j];
			}
		}

		return true;
	}


	public static void booleanProductWitness(int a[][], int b[][]){}



	public static void main(String[] args) {
		Graph g = new Graph();	    
	}
	   
}
