"use client";
import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import { Task } from "@/types";

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    const result = await apiClient.get<Task[]>("/tasks");
    if (result.success) {
      setTasks(result.data || []);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await apiClient.post("/tasks", { title, description });
    setTitle("");
    setDescription("");
    await fetchTasks();
    setLoading(false);
  };

  const handleToggle = async (id: string) => {
    await apiClient.patch(`/tasks/${id}/complete`);
    await fetchTasks();
  };

  const handleDelete = async (id: string) => {
    await apiClient.delete(`/tasks/${id}`);
    await fetchTasks();
  };

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-8">My Tasks</h1>
      <form onSubmit={handleCreateTask} className="mb-8 bg-white p-6 rounded-lg shadow">
        <input type="text" placeholder="Task title" value={title} onChange={(e) => setTitle(e.target.value)} className="w-full mb-4 p-2 border rounded" required />
        <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} className="w-full mb-4 p-2 border rounded" />
        <button type="submit" disabled={loading} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50">
          {loading ? "Creating..." : "Create Task"}
        </button>
      </form>
      <div className="grid gap-4">
        {tasks.map((task) => (
          <div key={task.id} className="bg-white p-6 rounded-lg shadow flex justify-between items-start">
            <div className="flex-1">
              <h3 className={`text-xl font-bold ${task.completed ? "line-through" : ""}`}>{task.title}</h3>
              {task.description && <p className="text-gray-600 mt-2">{task.description}</p>}
            </div>
            <div className="flex gap-2">
              <button onClick={() => handleToggle(task.id)} className={`px-4 py-2 rounded ${task.completed ? "bg-green-500" : "bg-gray-500"} text-white`}>
                {task.completed ? "Done" : "Pending"}
              </button>
              <button onClick={() => handleDelete(task.id)} className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
