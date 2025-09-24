class ListProducts():
    def __init__(self):
        self.products = []
    def add_product(self, p):
        self.products.append(p)
    def print_products(self):
        for p in self.products:
            print(p)
    def des_sort_product(self):
        for i in range(0,len(self.products)):
            for j in range(i+1,len(self.products)):
                pi=self.products[i]
                pj=self.products[j]
                if pi.price < pj.price:
                    self.products[j]=pi
                    self.products[i]=pj

    def des_sort_product2(self):
        sorted_products = sorted(self.products, key=lambda p: p.price, reverse=True)
        self.products = sorted_products

    # def des_sort_product2(self):
    #     def quicksort(arr):
    #         if len(arr) <= 1:
    #             return arr
    #         pivot = arr[0]
    #         left = [x for x in arr[1:] if x.price > pivot.price]
    #         right = [x for x in arr[1:] if x.price <= pivot.price]
    #         return quicksort(left) + [pivot] + quicksort(right)
    #
    #     self.products = quicksort(self.products)







