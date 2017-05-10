#include<iostream>
#include<cstdlib>
#include<string>
#include<sstream>
#include<algorithm>
#include<map>
#include<utility>
#include<list>
#include<limits.h>
#include<stdio.h>
using namespace std;

int main(){
    string line;
    string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; // reference for output
    int numEdges;
    int weight;
    getline(cin, line);
    while(1){
        /* read input into distance matrix */

        istringstream ipp(line);
        ipp >> numEdges;
        int matrix[numEdges][numEdges];
        for (int i = 0; i < numEdges; i++){
            getline(cin, line);
            istringstream iss(line);
            for(int j = 0; j < numEdges; j++){
                iss >> weight;
                if(weight == -1)
                    matrix[i][j] = 0;
                else
                    matrix[i][j] = weight;
            }
        }
        
        /* find minimum weight */
        int parent[numEdges];   // array for MST
        int key[numEdges];      // array used to get minimum weight edge in cut
        bool mst[numEdges];     // array for vertices not included in MST

        // initialize all keys as infinite
        // initialize all vertices not visited
        for(int i = 0; i < numEdges; i++){
            key[i] = INT_MAX;
            mst[i] = false;
        }

        key[0] = 0;
        parent[0] = -1;

        for(int count = 0; count < numEdges -1; count++){
            // get min key of vertex that hasnt been used yet
            // each iteration finds the lowest edge currently possible
            int min = INT_MAX, min_index;
            for(int v = 0; v < numEdges; v++){
                if(mst[v] == false && key[v] < min){
                    min = key[v];
                    min_index = v;
                }
            }
            int u = min_index;

            mst[u] = true;

            for(int v = 0; v < numEdges; v++){
                if(matrix[u][v] && mst[v] == false && matrix[u][v] < key[v]){
                    parent[v] = u;
                    key[v] = matrix[u][v];

                }
            }
        }
        int total = 0;
        for(int i = 1; i < numEdges; i++){
            total+= matrix[i][parent[i]];
        }
        cout << total << endl;
        list<pair<char, char>> edges;
        for(int i = 1; i < numEdges; i++){
            edges.push_back({alphabet[parent[i]], alphabet[i]});
        }
        for(auto &p : edges){
            if(p.first > p.second){
                int temp = p.first;
                p.first = p.second;
                p.second = temp;
            }
        }
        edges.sort();
        for(auto &p : edges)
            cout << p.first << p.second << endl;

        
        /* if there is another line, continue, otherwise exit */
        if(getline(cin, line)) {
            cout << endl;
            continue;
        }
        else break;
    }
    return 0;
}

