"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api";
import { Task } from "@/types";
import { Sidebar } from "@/components/Layout/Sidebar";
import { Header } from "@/components/Layout/Header";
import { TaskCard } from "@/components/Tasks/TaskCard";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SearchBar } from "@/components/Search/SearchBar";
import { Badge } from "@/components/ui/badge";

export default function DashboardPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [filterStatus, setFilterStatus] = useState<"all" | "pending" | "completed">("all");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("auth_token");
    if (!token) {
      router.push("/auth/signin");
      return;
    }

    setIsMounted(true);
    fetchTasks();
  }, [router]);

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
    const result = await apiClient.get<Task[]>("/tasks");
    if (result.success) {
      setTasks(result.data || []);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
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
    if (confirm("Are you sure you want to delete this task?")) {
      await apiClient.delete(`/tasks/${id}`);
      await fetchTasks();
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("refresh_token");
    router.push("/auth/signin");
  };

  if (!isMounted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center">
        <div className="animate-spin h-12 w-12 rounded-full border-4 border-primary-200 border-t-primary-600"></div>
      </div>
    );
  }

  const completedCount = tasks.filter(t => t.completed).length;
  const pendingCount = tasks.filter(t => !t.completed).length;

  const sidebarItems = [
    { label: "Dashboard", href: "/dashboard", icon: "📊", active: true, badge: null },
    { label: "Tasks", href: "#", icon: "📋", active: false, badge: pendingCount > 0 ? `${pendingCount}` : null },
    { label: "Settings", href: "#", icon: "⚙️", active: false, badge: null },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex">
      {/* Sidebar */}
      <Sidebar
        items={sidebarItems}
        title="TaskPilotAI"
        onLogout={handleLogout}
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
          <div className="p-6 md:p-8 max-w-7xl mx-auto w-full">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
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
            <Card className="mb-8">
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
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <div className="flex-1">
                <SearchBar
                  placeholder="Search tasks..."
                  onSearch={(query) => setSearchQuery(query)}
                />
              </div>
              <div className="flex gap-2 flex-wrap">
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
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
