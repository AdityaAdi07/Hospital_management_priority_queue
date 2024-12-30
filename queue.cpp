#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX 100

// Structure for a patient in the Binary Search Tree
typedef struct Patient {
    int id;
    char name[50];
    int severity;
    struct Patient *left, *right;
} Patient;

// Structure for Priority Queue Node
typedef struct PriorityNode {
    int id;
    char name[50];
    int severity;
    struct PriorityNode *next;
} PriorityNode;

// Graph for hospital navigation
int hospitalGraph[MAX][MAX];
int numDepartments;

// Create a new patient node for BST
Patient *createPatient(int id, char name[], int severity) {
    Patient *newPatient = (Patient *)malloc(sizeof(Patient));
    newPatient->id = id;
    strcpy(newPatient->name, name);
    newPatient->severity = severity;
    newPatient->left = newPatient->right = NULL;
    return newPatient;
}

// Insert patient into BST
Patient *insertPatient(Patient *root, int id, char name[], int severity) {
    if (!root)
        return createPatient(id, name, severity);
    if (id < root->id)
        root->left = insertPatient(root->left, id, name, severity);
    else if (id > root->id)
        root->right = insertPatient(root->right, id, name, severity);
    return root;
}

// Inorder traversal of BST
void inorderTraversal(Patient *root) {
    if (root) {
        inorderTraversal(root->left);
        printf("ID: %d, Name: %s, Severity: %d\n", root->id, root->name, root->severity);
        inorderTraversal(root->right);
    }
}

// Create a new node for Priority Queue
PriorityNode *createPriorityNode(int id, char name[], int severity) {
    PriorityNode *newNode = (PriorityNode *)malloc(sizeof(PriorityNode));
    newNode->id = id;
    strcpy(newNode->name, name);
    newNode->severity = severity;
    newNode->next = NULL;
    return newNode;
}

// Insert into Priority Queue based on severity
PriorityNode *insertPriorityQueue(PriorityNode *head, int id, char name[], int severity) {
    PriorityNode *newNode = createPriorityNode(id, name, severity);
    if (!head || severity > head->severity) {
        newNode->next = head;
        return newNode;
    }
    PriorityNode *current = head;
    while (current->next && current->next->severity >= severity)
        current = current->next;
    newNode->next = current->next;
    current->next = newNode;
    return head;
}

// Dequeue from Priority Queue
PriorityNode *dequeuePriorityQueue(PriorityNode *head) {
    if (!head)
        return NULL;
    PriorityNode *temp = head;
    head = head->next;
    free(temp);
    return head;
}

// Display Priority Queue
void displayPriorityQueue(PriorityNode *head) {
    while (head) {
        printf("ID: %d, Name: %s, Severity: %d\n", head->id, head->name, head->severity);
        head = head->next;
    }
}

// Dijkstra's algorithm for shortest path in hospital navigation
void dijkstra(int graph[MAX][MAX], int src, int dest, int n) {
    int dist[MAX], visited[MAX], parent[MAX];
    for (int i = 0; i < n; i++) {
        dist[i] = INT_MAX;
        visited[i] = 0;
        parent[i] = -1;
    }
    dist[src] = 0;

    for (int count = 0; count < n - 1; count++) {
        int min = INT_MAX, u;
        for (int v = 0; v < n; v++)
            if (!visited[v] && dist[v] < min)
                min = dist[v], u = v;

        visited[u] = 1;

        for (int v = 0; v < n; v++)
            if (!visited[v] && graph[u][v] && dist[u] != INT_MAX && dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
                parent[v] = u;
            }
    }

    // Display the shortest path
    printf("Shortest path from department %d to %d: ", src, dest);
    int path[MAX], index = 0, temp = dest;
    while (temp != -1) {
        path[index++] = temp;
        temp = parent[temp];
    }
    for (int i = index - 1; i >= 0; i--)
        printf("%d%s", path[i], i == 0 ? "\n" : " -> ");
    printf("Distance: %d\n", dist[dest]);
}

int main() {
    Patient *root = NULL;
    PriorityNode *queueHead = NULL;
    int choice;

    do {
        printf("\nHospital Management System\n");
        printf("1. Add Patient\n");
        printf("2. Display All Patients (BST)\n");
        printf("3. Add Patient to Priority Queue\n");
        printf("4. Serve Next Patient (Dequeue)\n");
        printf("5. Display Priority Queue\n");
        printf("6. Shortest Path Between Departments\n");
        printf("7. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
        case 1: {
            int id, severity;
            char name[50];
            printf("Enter Patient ID: ");
            scanf("%d", &id);
            printf("Enter Patient Name: ");
            scanf("%s", name);
            printf("Enter Severity (1-10): ");
            scanf("%d", &severity);
            root = insertPatient(root, id, name, severity);
            break;
        }
        case 2:
            printf("\nPatient Records (Inorder Traversal):\n");
            inorderTraversal(root);
            break;
        case 3: {
            int id, severity;
            char name[50];
            printf("Enter Patient ID: ");
            scanf("%d", &id);
            printf("Enter Patient Name: ");
            scanf("%s", name);
            printf("Enter Severity (1-10): ");
            scanf("%d", &severity);
            queueHead = insertPriorityQueue(queueHead, id, name, severity);
            break;
        }
        case 4:
            queueHead = dequeuePriorityQueue(queueHead);
            printf("Next patient served.\n");
            break;
        case 5:
            printf("\nPriority Queue:\n");
            displayPriorityQueue(queueHead);
            break;
        case 6: {
            int src, dest;
            printf("Enter number of departments: ");
            scanf("%d", &numDepartments);
            printf("Enter adjacency matrix for %d departments:\n", numDepartments);
            for (int i = 0; i < numDepartments; i++)
                for (int j = 0; j < numDepartments; j++)
                    scanf("%d", &hospitalGraph[i][j]);
            printf("Enter source department: ");
            scanf("%d", &src);
            printf("Enter destination department: ");
            scanf("%d", &dest);
            dijkstra(hospitalGraph, src, dest, numDepartments);
            break;
        }
        case 7:
            printf("Exiting...\n");
            break;
        default:
            printf("Invalid choice. Try again.\n");
        }
    } while (choice != 7);

    return 0;
}