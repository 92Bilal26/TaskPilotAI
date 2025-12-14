"use client";
import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import { useAuth } from "@/lib/useAuth";
import { useToast } from "@/lib/useToast";
import { Task } from "@/types";
import { Sidebar } from "@/components/Layout/Sidebar";
import { Header } from "@/components/Layout/Header";
import { TaskCard } from "@/components/Tasks/TaskCard";
import { TaskEditModal } from "@/components/Tasks/TaskEditModal";
import { Toast } from "@/components/Toast/Toast";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SearchBar } from "@/components/Search/SearchBar";
import { Badge } from "@/components/ui/badge";

export default function DashboardPage() {
  const { isAuthenticated, isLoading: authLoading, logout } = useAuth();
  const { toasts, removeToast, success, error } = useToast();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [filterStatus, setFilterStatus] = useState<"all" | "pending" | "completed">("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      setIsMounted(true);
      fetchTasks();
    }
  }, [authLoading, isAuthenticated]);

  // Filter tasks based on status and search
  useEffect(() => {
    let filtered = tasks;

    // Filter by status
    if (filterStatus === "pending") {
      filtered = filtered.filter(t => !t.completed);
    } else if (filterStatus === "completed") {
      filtered = filtered.filter(t => t.completed);
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(t =>
        t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (t.description && t.description.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    setFilteredTasks(filtered);
  }, [tasks, filterStatus, searchQuery]);

  const fetchTasks = async () => {
    const result = await apiClient.getTasks();
    if (result.success) {
      setTasks(result.data || []);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    setLoading(true);
    const result = await apiClient.createTask(title, description);
    if (result.success) {
      setTitle("");
      setDescription("");
      success("Task created successfully!");
      await fetchTasks();
    } else {
      error(result.error || "Failed to create task");
    }
    setLoading(false);
  };

  const handleToggle = async (id: string) => {
    const result = await apiClient.toggleTask(id);
    if (result.success) {
      await fetchTasks();
    } else {
      error(result.error || "Failed to update task");
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm("Are you sure you want to delete this task?")) {
      const result = await apiClient.deleteTask(id);
      if (result.success) {
        success("Task deleted successfully!");
        await fetchTasks();
      } else {
        error(result.error || "Failed to delete task");
      }
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
  };

  const handleSaveEdit = async (updates: { title: string; description: string }) => {
    if (!editingTask) return;
    const result = await apiClient.updateTask(editingTask.id, updates);
    if (result.success) {
      setEditingTask(null);
      success("Task updated successfully!");
      await fetchTasks();
    } else {
      error(result.error || "Failed to update task");
    }
  };

  if (!isMounted || authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center animate-fade-in">
        <div className="animate-spin h-12 w-12 rounded-full border-4 border-primary-200 border-t-primary-600"></div>
      </div>
    );
  }

  const completedCount = tasks.filter(t => t.completed).length;
  const pendingCount = tasks.filter(t => !t.completed).length;

  const sidebarItems = [
    { label: "Dashboard", href: "/dashboard", icon: "📊", active: true, badge: null },
    { label: "Tasks", href: "/dashboard/tasks", icon: "📋", active: false, badge: pendingCount > 0 ? `${pendingCount}` : null },
    { label: "Settings", href: "/dashboard/settings", icon: "⚙️", active: false, badge: null },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex flex-col md:flex-row pb-20 md:pb-0">
      {/* Sidebar */}
      <Sidebar
        items={sidebarItems}
        title="TaskPilotAI"
        onLogout={logout}
        collapsed={sidebarCollapsed}
        onCollapsedChange={setSidebarCollapsed}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header
          title="Task Dashboard"
          subtitle="Manage and organize your tasks efficiently"
          action={
            <Button onClick={() => window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" })}>
              + New Task
            </Button>
          }
        />

        {/* Content Area */}
        <div className="flex-1 overflow-auto">
          <div className="p-4 sm:p-6 md:p-8 max-w-7xl mx-auto w-full">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 mb-6 sm:mb-8">
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500 font-medium">Total Tasks</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">{tasks.length}</p>
                    </div>
                    <div className="w-14 h-14 bg-primary-100 rounded-xl flex items-center justify-center text-2xl">
                      📋
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500 font-medium">Pending</p>
                      <p className="text-3xl font-bold text-warning-600 mt-2">{pendingCount}</p>
                    </div>
                    <div className="w-14 h-14 bg-warning-100 rounded-xl flex items-center justify-center text-2xl">
                      ⏳
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500 font-medium">Completed</p>
                      <p className="text-3xl font-bold text-success-600 mt-2">{completedCount}</p>
                    </div>
                    <div className="w-14 h-14 bg-success-100 rounded-xl flex items-center justify-center text-2xl">
                      ✅
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Create Task Card */}
            <Card className="mb-6 sm:mb-8">
              <CardHeader>
                <CardTitle>Create New Task</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleCreateTask} className="space-y-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Task Title</label>
                    <Input
                      type="text"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      placeholder="What do you need to accomplish?"
                      disabled={loading}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Description (Optional)</label>
                    <Textarea
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                      placeholder="Add more details about this task..."
                      disabled={loading}
                    />
                  </div>
                  <Button type="submit" disabled={loading} className="w-full">
                    {loading ? (
                      <span className="flex items-center justify-center gap-2">
                        <div className="animate-spin h-4 w-4 rounded-full border-2 border-white border-t-transparent"></div>
                        Creating...
                      </span>
                    ) : (
                      "Create Task"
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Filter & Search */}
            <div className="flex flex-col gap-3 sm:gap-4 mb-6">
              <div className="w-full">
                <SearchBar
                  placeholder="Search tasks..."
                  onSearch={(query) => setSearchQuery(query)}
                />
              </div>
              <div className="flex gap-2 flex-wrap justify-start sm:justify-between">
                <Badge
                  variant={filterStatus === "all" ? "default" : "outline"}
                  className="cursor-pointer"
                  onClick={() => setFilterStatus("all")}
                >
                  All ({tasks.length})
                </Badge>
                <Badge
                  variant={filterStatus === "pending" ? "default" : "outline"}
                  className="cursor-pointer"
                  onClick={() => setFilterStatus("pending")}
                >
                  Pending ({pendingCount})
                </Badge>
                <Badge
                  variant={filterStatus === "completed" ? "default" : "outline"}
                  className="cursor-pointer"
                  onClick={() => setFilterStatus("completed")}
                >
                  Done ({completedCount})
                </Badge>
              </div>
            </div>

            {/* Tasks List */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                {filterStatus === "all" && "Your Tasks"}
                {filterStatus === "pending" && "Pending Tasks"}
                {filterStatus === "completed" && "Completed Tasks"}
              </h2>

              {filteredTasks.length === 0 ? (
                <Card className="p-12 text-center">
                  <div className="text-5xl mb-4">📭</div>
                  <p className="text-gray-500 text-lg">No tasks found</p>
                  <p className="text-gray-400 text-sm mt-2">
                    {searchQuery ? "Try a different search term" : "Create one to get started!"}
                  </p>
                </Card>
              ) : (
                <div className="space-y-3">
                  {filteredTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onComplete={() => handleToggle(task.id)}
                      onDelete={() => handleDelete(task.id)}
                      onEdit={handleEditTask}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Edit Modal */}
      <TaskEditModal
        task={editingTask}
        onClose={() => setEditingTask(null)}
        onSave={handleSaveEdit}
        isLoading={loading}
      />

      {/* Toasts */}
      <Toast messages={toasts} onRemove={removeToast} />
    </div>
  );
}
