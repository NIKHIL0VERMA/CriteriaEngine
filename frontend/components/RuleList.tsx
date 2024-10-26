import React, { useState, useEffect } from 'react';
import { Pencil, X } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from "c/components/ui/dialog";
import { Button } from "c/components/ui/button";
import { Input } from "c/components/ui/input";
import { Textarea } from "c/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "c/components/ui/card";
import { toast } from "c/hooks/use-toast";

interface Rule {
  id: string;
  name: string;
  description: string;
  rule_string: string;
  created_at: string;
}

const RuleList: React.FC = () => {
  const [rules, setRules] = useState<Rule[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [editingRule, setEditingRule] = useState<Rule | null>(null);
  const [editFormData, setEditFormData] = useState<{ name: string; description: string; rule_string: string }>({
    name: '',
    description: '',
    rule_string: ''
  });
  const [editError, setEditError] = useState<string>('');
  const [editSuccess, setEditSuccess] = useState<string>('');
  const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);
  
  useEffect(() => {
    fetchRules();
  }, [page]);
  
  const fetchRules = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/fetch/?page=${page}&limit=5`);
      const data = await response.json();
      setRules(data.rules);
      setTotalPages(data.pages);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching rules:', error);
      setLoading(false);
    }
  };
  
  const handleEditClick = (rule: Rule) => {
    setEditingRule(rule);
    setEditFormData({
      name: rule.name,
      description: rule.description,
      rule_string: rule.rule_string
    });
    setIsDialogOpen(true);
  };
  
  const handleEditSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setEditError('');
    setEditSuccess('');
  
    try {
      const response = await fetch(`http://localhost:8000/api/v1/update/${editingRule?.id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editFormData),
      });
  
      if (!response.ok) {
        throw new Error('Failed to update rule');
      }
  
      toast({
        title: "Success",
        description: "Rule updated successfully!",
        duration: 3000,
      });
      fetchRules(); // Refresh the rules list
      setIsDialogOpen(false); // Close the dialog
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : 'An unknown error occurred',
        variant: "destructive",
        duration: 3000,
      });
    }
  };
  
  if (loading) {
    return <div className="text-center">Loading...</div>;
  }
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Rule List</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {rules.map((rule) => (
            <Card key={rule.id}>
              <CardContent className="p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-lg">{rule.name}</h3>
                    <p className="text-gray-600">{rule.description}</p>
                    <code className="block mt-2 bg-gray-50 p-2 rounded">{rule.rule_string}</code>
                    <div className="mt-2 text-sm text-gray-500">
                      Created: {new Date(rule.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => handleEditClick(rule)}>
                    <Pencil className="h-4 w-4 mr-2" />
                    Edit
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        <div className="mt-6 flex justify-center space-x-2">
          {Array.from({ length: totalPages }, (_, i) => (
            <Button
              key={i}
              onClick={() => setPage(i + 1)}
              variant={page === i + 1 ? "default" : "outline"}
            >
              {i + 1}
            </Button>
          ))}
        </div>
      </CardContent>
  
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Edit Rule</DialogTitle>
            <DialogClose asChild>
              <Button variant="ghost" size="icon">
                <X className="h-4 w-4" />
              </Button>
            </DialogClose>
          </DialogHeader>
          <form onSubmit={handleEditSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <Input
                value={editFormData.name}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEditFormData({ ...editFormData, name: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <Textarea
                value={editFormData.description}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setEditFormData({ ...editFormData, description: e.target.value })}
                rows={3}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Rule String</label>
              <Textarea
                value={editFormData.rule_string}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setEditFormData({ ...editFormData, rule_string: e.target.value })}
                rows={5}
                required
              />
            </div>
            <div className="flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">Update Rule</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </Card>
  );
};

export default RuleList;
