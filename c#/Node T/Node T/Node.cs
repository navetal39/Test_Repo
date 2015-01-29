using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Node_T
{
    class Node<T>
    {
        private T info;
        private Node<T> next;

        public Node(T x)
        {
            this.info = x;
        }
        public Node(Node<T> x)
        {
            this.info = x.GetInfo();
            if (x.GetNext() != null)
                this.next = new Node<T>(x.GetNext());
        }
        public Node(T x, Node<T> next)
        {
            this.info = x;
            this.next = next;
        }
        public T GetInfo()
        {
            return this.info;
        }
        public Node<T> GetNext()
        {
            return this.next;
        }
        public void SetInfo(T x)
        {
            this.info = x;
        }
        public void SetNext(Node<T> x)
        {
            this.next = x;
        }
        public override string ToString()
        {
            return "" + this.info;
        }
    }
}
